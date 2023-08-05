"""Environment keys for web environment."""
from emews.api.env_key import EnvironmentKey


class Observation(EnvironmentKey):
    """Observation environment key enums.  Observation key class must be named 'Observation'."""
    CRAWL_SITE = int
    LINK_CLICKED = int


class Evidence(EnvironmentKey):
    """Evidence environment key enums.  Evidence key class must be named 'Evidence'."""
    VIRAL_LINKS = int
