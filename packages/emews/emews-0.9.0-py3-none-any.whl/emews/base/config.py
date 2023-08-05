"""Configuration functions."""
from collections.abc import Collection, Mapping
import os

from ruamel.yaml import YAML


def get_root_path() -> str:
    """Return the eMews root directory.  This module is located under <eMews_root>/base."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def get_environments_path() -> str:
    """Return the environment path."""
    return os.path.abspath(os.path.join(get_root_path(), 'environments'))


def get_services_path() -> str:
    """Return the service path."""
    return os.path.abspath(os.path.join(get_root_path(), 'services'))


def parse(filename: str) -> dict:
    """Parse the given filename, and return a structure representative of the YAML."""
    with open(filename) as f:
        in_dict = YAML().load(f)

    return _to_raw_dict_process(in_dict)


def get_service_class_name(service_config: Mapping) -> str:
    """Return the service class name from the config, or the default if not specified."""
    return service_config.get('service_class', 'DefaultService')


def parse_service_config(service_name: str, service_config_filename: str) -> dict:
    """Parse the service configuration."""
    return parse(os.path.join(get_services_path(), service_name, f"{service_config_filename}.yml"))


def parse_system_config(node_config_path: str = None) -> dict:
    """Parse the system configuration."""
    root_path = get_root_path()

    # base system conf (non-user config - system-wide)
    base_config = parse(os.path.join(root_path, 'base', 'base_conf.yml'))
    # system conf (user config - system-wide)
    system_config = parse(os.path.join(root_path, 'system.yml'))
    # node conf (user config - per node)
    node_config = parse(node_config_path) if node_config_path is not None else {}

    # merge config dicts
    return _merge_configs(base_config['system'], system_config, node_config)


def _to_raw_dict_process(in_type):
    """Recursively process the input (Mapping)."""
    out_type = {}
    for key, value in in_type.items():
        if isinstance(value, Mapping):
            out_type[key] = _to_raw_dict_process(value)
        elif isinstance(value, Collection) and not isinstance(value, str):
            out_type[key] = _to_raw_list_process(value)
        else:
            # assume primitive type
            out_type[key] = value

    return out_type


def _to_raw_list_process(in_type):
    """Recursively process the input (Collection)."""
    out_type = []
    for value in in_type:
        if isinstance(value, Mapping):
            out_type.append(_to_raw_dict_process(value))
        elif isinstance(value, Collection) and not isinstance(value, str):
            out_type.append(_to_raw_list_process(value))
        else:
            # assume primitive type
            out_type.append(value)

    return out_type


# Config merging functions
def _merge_configs(*config_dicts):
    """
    Merge the input config files by key, in order of precedence.

    Precedence order: base config, system config, node config.
    For example, values in node config could override values in system config.
    """
    if len(config_dicts) < 2:
        # must be at least two dicts to merge
        raise ValueError("At least two dictionaries must be passed.")

    config_dict_iter = iter(config_dicts)
    base_config = next(config_dict_iter)  # first dict is assumed to be base config
    merged_dict = base_config['overrides']

    while True:
        try:
            config_dict = next(config_dict_iter)  # the next config dict in config_dicts
        except StopIteration:
            break

        if len(config_dict):
            merged_dict = _section_merge(merged_dict, config_dict)

    # add in the read-only options
    _section_update_readonly(base_config['readonly'], merged_dict)

    return merged_dict


def section_merge_by_name(config, *sections):
    """
    Merge all given section names from the given config.

    Return a new dict.  If a key exists in multiple sections, override the value with the current
    section to merge.
    """
    out_config = {}
    for section in sections:
        for key, val in config[section].items():
            out_config[key] = val

    return out_config


def _section_merge(sec1_dict, sec2_dict, keychain="root"):
    """
    Merge the first section with the second section.

    A section is a basic dict.
    """
    new_section = {}

    for s1_key, s1_val in sec1_dict.items():
        s2_val = sec2_dict.get(s1_key, None)

        cur_kc = keychain + "-->" + str(s1_key)

        if s2_val is None:
            new_section[s1_key] = s1_val
        elif isinstance(s1_val, Mapping):
            if not isinstance(s2_val, Mapping):
                raise TypeError(f"While merging configuration at {cur_kc}: Expected a section to "
                                f"merge with, instead got '{type(s2_val)}'")
            new_section[s1_key] = _section_merge(s1_val, s2_val, keychain=cur_kc)
        elif isinstance(s2_val, Mapping):
            raise TypeError(f"While merging configuration at {cur_kc}: Cannot merge a non-section "
                            f"({type(s1_val)}) with a section'")
        else:
            new_section[s1_key] = s2_val

    return new_section


def _section_update_readonly(readonly_sec, merged_sec):
    """
    Add the readonly keys to the merged dict.

    This is a recursive procedure; the section depth should not be that great.
    """
    for s_key, s_val in readonly_sec.items():
        if isinstance(s_val, Mapping):
            if s_key not in merged_sec:
                merged_sec[s_key] = {}
            _section_update_readonly(s_val, merged_sec[s_key])
        else:
            if s_key in merged_sec:
                raise ValueError(f"Cannot override values of read-only keys.  Key: '{s_val}'.")
            merged_sec[s_key] = s_val
