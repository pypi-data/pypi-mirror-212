"""
Environment keys for example environment.

This is a separate module to enable key importing without having to indirectly import env.  Only the hub needs to
import the environment module (env), not services running on hosts.
"""

from emews.api.env_key import EnvironmentKey


class Evidence(EnvironmentKey):
    """Evidence environment key enums.  Evidence key class must be named 'Evidence'."""
    HELLO_WORLD = int  # list type (observations and evidence can take zero or more values in a list)
