"""Environment for SiteCrawler.  Provides evidence for viral links."""
from typing import Dict, List, Set, Tuple

import socket
import struct

from emews.api.env import Environment
from emews.api.env_key import EnvironmentKey

from emews.environments.web.keys import Observation, Evidence


class WebEnv(Environment):
    """Classdocs."""

    __slots__ = ('_site_map', '_link_data', '_timer_data', '_viral_links', '_viral_link_threshold',
                 '_viral_link_expiration')

    # enums
    LINK_COUNT = 0
    LINK_VIRAL = 1

    def __init__(self):
        """Constructor."""
        super().__init__()

        self._site_map: Dict[int, int] = {}  # [node_id]: current site
        self._link_data: Dict[int, Dict[int, List]] = {}  # [site]: {[link_index]: link_data}
        self._timer_data: Dict[int, Tuple] = {}  # [timer_fd]: timer data
        self._viral_links: Dict[int, Set[int]] = {}  # [site]: set of viral links

        # viral link parameters
        self._viral_link_threshold = 10  # number of specific links clicks, per site, before viral
        self._viral_link_expiration = 60  # seconds that a link remains viral

    def update_evidence(self, node_id: int, obs_key: EnvironmentKey, obs_val) -> None:
        """Update evidence given new observation."""
        assert len(obs_val) == 1
        if obs_key == Observation.CRAWL_SITE:
            # node is starting a new crawl
            self._site_map[node_id] = obs_val[0]
        elif obs_key == Observation.LINK_CLICKED:
            # node clicked on a link
            self._update_clicked_links(node_id, obs_val[0])

    def get_evidence(self, node_id: int, ev_key: EnvironmentKey):
        """Return the relevant list of evidence given the key and a node id."""
        assert ev_key == Evidence.VIRAL_LINKS

        crawl_site = self._site_map.get(node_id)
        if crawl_site is None:
            return ()

        viral_links = self._viral_links.get(crawl_site)
        if viral_links is None:
            return ()

        return viral_links

    def _update_clicked_links(self, node_id: int, clicked_link: int):
        """Update relevant evidence in regard to a new click."""
        # New_obs.val is the link index clicked on.  Simply check if enough clicks have occurred.
        # The agent needs to send an observation on what site it is crawling before sending link clicks
        crawl_site = self._site_map[node_id]

        if crawl_site not in self._link_data:
            self._link_data[crawl_site] = {}

        link_data = self._link_data[crawl_site]  # link data is for a specific site

        if clicked_link not in link_data:
            link_data[clicked_link] = [0, False]  # [link index]: number of clicks, went viral?

        per_link_data = link_data[clicked_link]

        num_clicks = per_link_data[WebEnv.LINK_COUNT] + 1
        per_link_data[WebEnv.LINK_COUNT] = num_clicks

        if num_clicks > self._viral_link_threshold and not per_link_data[WebEnv.LINK_VIRAL]:
            # viral link, update evidence (used for agent ask)
            per_link_data[WebEnv.LINK_VIRAL] = True
            if crawl_site not in self._viral_links:
                self._viral_links[crawl_site] = set()

            self._viral_links[crawl_site].add(clicked_link)

            self.logger.info("link on server '%s' at index %d has gone viral",
                             socket.inet_ntoa(struct.pack(">I", crawl_site)), clicked_link)

            timer_fd = self.new_timer(self._viral_link_expiration, self._evidence_viral_link_expired, repeat=False)
            self._timer_data[timer_fd] = (crawl_site, clicked_link)

    def _evidence_viral_link_expired(self, timer_fd: int, num_expires: int):
        """When a timer has finished, this will be invoked."""
        crawl_site, link_index = self._timer_data[timer_fd]
        self._viral_links[crawl_site].remove(link_index)

        self.del_timer(timer_fd)

        self.logger.info("link on server '%s' at index '%d' is no longer viral",
                         socket.inet_ntoa(struct.pack(">I", crawl_site)), link_index)
