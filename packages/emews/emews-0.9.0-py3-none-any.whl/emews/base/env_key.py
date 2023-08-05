"""
Base module for eMews network environments key structures.

This is a separate module to enable key importing without having to indirectly import env.  Only the hub needs to
import the environment module.
"""
from typing import Tuple, Union

from enum import Enum
import inspect
import os

ENV_KEY_BASE_TYPES = Union[bool, int, float]
ENV_KEY_TYPE = Tuple[ENV_KEY_BASE_TYPES, ...]

_ENV_KEY_IDX = 1  # free index for environment keys


class EnvironmentKey(Enum):
    """Environment observation and evidence key definitions."""

    def __new__(cls, key_list_type: ENV_KEY_BASE_TYPES):
        """Member value assigned, key types are passed in."""
        if key_list_type == bool:
            pack_type = '?'
        elif key_list_type == int:
            pack_type = 'l'
        elif key_list_type == float:
            pack_type = 'd'
        else:
            raise AttributeError(f"key list type '{key_list_type}' is not supported.  Use 'bool', 'int', or 'float'")

        global _ENV_KEY_IDX
        value = _ENV_KEY_IDX  # key id
        _ENV_KEY_IDX += 1

        # this is the module which contains the keys.py file
        _, key_parent_module, keys_module = inspect.getfile(cls).rsplit(os.sep, 2)

        if keys_module != 'keys.py':
            raise AttributeError("child EnvironmentKey class must be in a module named 'keys.py' "
                                 f"(given module name: {keys_module})")

        if cls.__name__ == 'Observation':
            key_type_abbrev = 'o'
        elif cls.__name__ == 'Evidence':
            key_type_abbrev = 'e'
        else:
            raise AttributeError("child EnvironmentKey class must be named 'Observation' or "
                                 f"'Evidence' (given class name: {cls.__name__})")

        obj = object.__new__(cls)
        obj._value_ = value
        obj.key_list_type = pack_type

        # this sets the full path name for the key, used with key name as a global identifier
        obj.key_env_path = f"{key_parent_module}.{key_type_abbrev}"
        return obj

    def key_full_name(self) -> str:
        """
        Return the full name of the key.

        This name is globally unique among all keys, and provides a means to lookup key ids.
        """
        return f"{self.key_env_path}.{self.name}"
