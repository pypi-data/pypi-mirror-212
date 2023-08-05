"""Web crawler with environment support for link selection based on popularity."""
from typing import AnyStr, List, Set, Tuple, Union

import logging
import math
import random
import socket
import struct

import bs4
from urllib.parse import urljoin, urlparse
import urllib3

from emews.environments.web.keys import Observation, Evidence
from emews.api.service import Service
from emews.api.random import TruncnormInt, UniformInt


class AgentModel:
    """Next link sampler."""

    __slots__ = ('logger', 'prior', 'ev_viral', 'ev_visited', 'num_pref_links')

    def __init__(self, logger: logging.Logger):
        """Constructor."""
        self.logger = logger

        self.prior: List[float] = [0.0] * 2  # class variable
        self.ev_viral: List[float] = [0.0] * 2  # attribute variables
        self.ev_visited: List[float] = [0.0] * 2
        self.num_pref_links = 0

    def _set_prior_param(self, num_links: int, links_preferred: List[int], links_preferred_strength: float):
        """Set the prior."""
        num_pref_links = 0
        for index in links_preferred:
            if 0 <= index < num_links:
                num_pref_links += 1

        norm = ((num_pref_links * links_preferred_strength) + num_links - num_pref_links) / float(num_links)

        self.num_pref_links = num_pref_links
        self.prior[0] = links_preferred_strength / (num_links * norm)
        self.prior[1] = 1.0 / (num_links * norm)

    def _set_evidence_params(self, num_links: int, link_viral_strength: float, link_visited_strength: float):
        """Set the evidence variable parameters."""
        norm = (link_viral_strength + num_links - 1.0) / float(num_links)
        self.ev_viral[0] = link_viral_strength / (num_links * norm)
        self.ev_viral[1] = 1.0 / (num_links * norm)

        norm = (link_visited_strength + num_links - 1.0) / float(num_links)
        self.ev_visited[0] = link_visited_strength / (num_links * norm)
        self.ev_visited[1] = 1.0 / (num_links * norm)

    @staticmethod
    def _prob_to_log(prob: float) -> float:
        """Convert a probability to a log prob."""
        if prob > 0.0:
            return math.log(prob)  # base e

        return -28.0  # represent an arbitarily small probability

    def sample(self, num_links: int, links_preferred: List[int], visited_links: Set[int],
               viral_links: Tuple[int]) -> int:
        """Perform inference on the factored joint, and sample."""
        prob_to_log = self._prob_to_log
        log_prior_pref = prob_to_log(self.prior[0])
        log_prior_nonpref = prob_to_log(self.prior[1])
        log_viral = prob_to_log(self.ev_viral[0])
        log_nonviral = prob_to_log(self.ev_viral[1])
        log_visited = prob_to_log(self.ev_visited[0])
        log_nonvisited = prob_to_log(self.ev_visited[1])

        posteriors: List[float] = []
        # init to appropriate prior
        for i in range(num_links):
            if i in links_preferred:
                posteriors.append(log_prior_pref)
            else:
                posteriors.append(log_prior_nonpref)

        for i in range(num_links):
            # for each link in prior (links to click)
            nonviral_count = num_links
            nonvisited_count = num_links
            if i in viral_links:
                # if the link at index i is viral, append viral prob for evidence node i
                # Note that we only do this once per index i, even if multiple videos are viral.
                # This is a consequence of the naive Bayes assumption.
                posteriors[i] += log_viral
                nonviral_count -= 1  # the link at index i is viral, so decrement
            if i in visited_links:
                posteriors[i] += log_visited
                nonvisited_count -= 1

            posteriors[i] += nonviral_count * log_nonviral
            posteriors[i] += nonvisited_count * log_nonvisited

        # find the normalization constant, P(e).  Because we are in log space we gotta be sneaky.
        # First, find the smallest log and pre-normalize the others with it, then, exponentiate
        smallest_posterior = min(posteriors)

        for i in range(len(posteriors)):
            posteriors[i] -= smallest_posterior
            if posteriors[i] < -21:
                # anything smaller than this may cause underflow issues, treat as exp(zero) = 1
                posteriors[i] = 1.0
            else:
                posteriors[i] = math.exp(posteriors[i])

        norm = 1.0 / math.fsum(posteriors)  # p(e)

        # normalize posteriors
        for i in range(len(posteriors)):
            posteriors[i] = posteriors[i] * norm

        self.logger.debug("Agent Model: posterior: %s", posteriors)

        # sample link index from the posterior CDF
        r_sample = random.random()  # [0.0, 1.0)
        cdf_posterior = 0.0
        selected_link_index = 0
        for posterior in posteriors:
            cdf_posterior += posterior
            if cdf_posterior > r_sample:
                # sample is within this interval, corresponds to the link index
                break
            selected_link_index += 1

        # self.logger.debug("SAMPLE: link index (%d/%d), random_sample: %f", selected_link_index, num_links, r_sample)
        return selected_link_index

    def update_model(self, num_links: int, links_preferred: List[int], links_preferred_strength: float,
                     link_viral_strength: float, link_visited_strength: float):
        """Build the model based on the number of links.  Evidence count is consistent."""
        # rebuild prior (class) distribution
        self._set_prior_param(num_links, links_preferred, links_preferred_strength)
        # rebuild conditional distributions
        self._set_evidence_params(num_links, link_viral_strength, link_visited_strength)
        self.logger.debug("Agent Model: attributes (prior): pref=%f, not_pref=%f "
                          "(state_space=2, num_attributes=%d, num_pref_links=%d)",
                          self.prior[0], self.prior[1], num_links, self.num_pref_links)
        self.logger.debug(
            "Agent Model: attributes (evidence): viral=%f, not_viral=%f (state_space=2, num_attributes=%d)",
            self.ev_viral[0], self.ev_viral[1], num_links)
        self.logger.debug(
            "Agent Model: attributes (evidence): visited=%f, not_visited=%f (state_space=2, num_attributes=%d)",
            self.ev_visited[0], self.ev_visited[1], num_links)


class BaseCrawler(Service):
    """Base class for web crawling clients."""

    __slots__ = ('_http',
                 '_invalid_link_prefixes',
                 '_siteURLs',
                 '_std_deviation_link',
                 '_site_sampler',
                 '_crawl_sampler',
                 '_num_links_sampler',
                 '_link_delay_sampler')

    def __init__(self, config: dict):
        """Constructor."""
        super().__init__()

        self._invalid_link_prefixes: List[str] = config['invalid_link_prefixes']
        self._siteURLs: List[str] = config['start_sites']

        self._site_sampler = UniformInt(upper_bound=len(self._siteURLs) - 1)
        self._num_links_sampler = UniformInt(**config['num_links_sampler'])
        self._crawl_sampler = UniformInt(**config['crawl_sampler'])
        self._link_delay_sampler = UniformInt(**config['link_delay_sampler'])

        # urllib3 related setup
        urllib3.disable_warnings()  # ignore self-signed SSL certs
        br_header = urllib3.util.make_headers(user_agent=config['user_agent'])
        self._http = urllib3.PoolManager(num_pools=2, headers=br_header, cert_reqs='CERT_NONE')

    def get_next_link_index(self, page_links: List[str]) -> int:
        """Given a list of page links, find and return the index of the first valid link."""
        raise NotImplementedError

    def service_run(self) -> None:
        """Run the service."""
        while not self.interrupted():
            self.sleep(self._crawl_sampler.sample())
            self._crawl(self._siteURLs[self._site_sampler.sample()])

    def _checklink(self, link_str: Union[str, None]) -> bool:
        """Check a link object's URL for validity (not a javascript link or something)."""
        if link_str is None:
            return False

        for prefix in self._invalid_link_prefixes:
            if link_str.lower().startswith(prefix):
                return False

        return True

    def _get_page_links(self, site_url: str, raw_html: AnyStr) -> List[str]:
        """Parse a list of links from the raw HTML."""
        soup_html = bs4.BeautifulSoup(raw_html, 'html.parser')  # using standard python html parser

        page_links: List[str] = []
        for page_link in soup_html.find_all('a'):
            if self._checklink(page_link.get('href')):
                page_links.append(urljoin(site_url, page_link.get('href')))

        return page_links

    def _crawl(self, site_host):
        """Web crawl, starting from the _siteURL, picking links from each page visited."""
        num_links_to_crawl = self._num_links_sampler.sample()

        self.logger.info("Will crawl maximum of %d pages", num_links_to_crawl)

        page_url = site_host
        crawl_str = f"Starting crawl at {site_host}"

        num_pages_visited = 0

        # now crawl for (max) num_links_to_crawl
        for _ in range(num_links_to_crawl):
            self.sleep(self._link_delay_sampler.sample())
            self.logger.info(crawl_str)

            try:
                site_page = self._http.request('GET', page_url).data
            except Exception as ex:
                self.logger.warning("On site open: %s, (server: %s)", ex, site_host)
                return

            num_pages_visited += 1
            site_page_links = self._get_page_links(site_host, site_page)

            if not site_page_links:
                self.logger.debug("Crawled page '%s' doesn't have any links to click.", page_url)
                break

            selected_link_index = self.get_next_link_index(site_page_links)

            page_url = site_page_links[selected_link_index]
            link_split = urlparse(bytes(page_url, 'utf_8'))
            site_host: str = f"{link_split.scheme.decode()}://{link_split.netloc.decode()}"

            crawl_str = f"Clicked link [{selected_link_index}/{len(site_page_links) - 1}]: {page_url}"

        self.logger.info("Finished crawl at %s (pages visited: %d)", site_host, num_pages_visited)


class DefaultService(BaseCrawler):
    """Web crawler client."""

    __slots__ = ('_first_page',
                 '_next_link_sigma_first',
                 '_next_link_sigma')

    def __init__(self, config: dict):
        """Constructor."""
        super().__init__(config)

        self._first_page = True
        self._next_link_sigma_first: float = config['next_link_sigma_first']
        self._next_link_sigma: float = config['next_link_sigma']

    def get_next_link_index(self, page_links: List[str]) -> int:
        """Given a list of page links, find and return the index of the first valid link."""
        if self._first_page:
            self._first_page = False
            std_deviation = self._next_link_sigma_first
        else:
            std_deviation = self._next_link_sigma

        if len(page_links) == 1:
            return 0

        selected_link_index = TruncnormInt(upper_bound=len(page_links) - 1, sigma=std_deviation).sample()

        return selected_link_index


class AgentCrawler(BaseCrawler):
    """Web crawler that interacts with its environment."""

    __slots__ = ('_link_viral_strength',
                 '_link_visited_strength',
                 '_next_link_model',
                 '_links_preferred',
                 '_links_preferred_strength',
                 '_visited_links')

    def __init__(self, config: dict):
        """Constructor."""
        super().__init__(config)

        self._links_preferred: List[int] = config['links_preferred']

        self._links_preferred_strength: float = config['links_preferred_strength']
        self._link_viral_strength: float = config['link_viral_strength']
        self._link_visited_strength: float = config['link_visited_strength']

        self._next_link_model = AgentModel(self.logger)

        self._visited_links: Set[int] = set()  # local evidence

    def service_run(self) -> None:
        """Run the service."""
        while not self.interrupted():
            self.sleep(self._crawl_sampler.sample())

            site_host = self._siteURLs[self._site_sampler.sample()]
            # Important: the agent assumes the site visited doesn't change, ie, video hosting site.
            # The site to crawl should not contain external links.
            crawl_ip: Tuple = struct.unpack(">I", socket.inet_aton(site_host.rsplit('/', 1)[-1]))
            self.tell(Observation.CRAWL_SITE, crawl_ip)  # tell environment the site we are going to crawl

            self._crawl(site_host)

            self._visited_links.clear()

    def get_next_link_index(self, page_links: List[str]) -> int:
        """Given a list of page links, find and return the index of the first valid link."""
        self._next_link_model.update_model(len(page_links), self._links_preferred, self._links_preferred_strength,
                                           self._link_viral_strength, self._link_visited_strength)

        ev_visited_links = self._visited_links
        ev_viral_links = self.ask(Evidence.VIRAL_LINKS)

        self.logger.debug("Current evidence (viral link indices): %s", ev_viral_links)

        selected_link_index = self._next_link_model.sample(len(page_links), self._links_preferred, ev_visited_links,
                                                           ev_viral_links)

        self.tell(Observation.LINK_CLICKED, (selected_link_index,))
        ev_visited_links.add(selected_link_index)

        return selected_link_index
