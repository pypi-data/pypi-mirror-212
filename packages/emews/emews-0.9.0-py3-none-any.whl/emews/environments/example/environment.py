"""
Example environment.  Returns evidence as a request count when asked.

This environment does not implement observations.  See HelloWorld service for example of environment usage.
"""
from emews.api.env import Environment
from emews.api.env_key import EnvironmentKey

from emews.environments.example.keys import Evidence


class ExampleEnv(Environment):
    """Example environment.  Can be named anything, but only one can exist per module."""

    def __init__(self):
        """Constructor."""
        self._ev_req_count = 0  # note, no __slots__() as base Enum doesn't use them

    def get_evidence(self, node_id: int, ev_key: EnvironmentKey):
        """Return evidence based on given evidence key."""
        assert ev_key == Evidence.HELLO_WORLD

        self._ev_req_count += 1

        return self._ev_req_count,

    def update_evidence(self, node_id: int, obs_key: EnvironmentKey, obs_val) -> None:
        pass
