"""eMews node CORE ConfigServices."""
from typing import Any, Dict, List

import pathlib

from core.config import Configuration, ConfigString
from core.configservice.base import ConfigService, ConfigServiceMode

GROUP_NAME: str = "eMews"


class EmewsNodeHub(ConfigService):
    """eMews Hub Node."""

    name: str = "HubNode"
    group: str = GROUP_NAME
    directories: List[str] = []
    files: List[str] = ["emews_node_hub.sh"]
    executables: List[str] = ["python3"]
    dependencies: List[str] = []
    startup: List[str] = ["sh emews_node_hub.sh"]
    validate: List[str] = []
    shutdown: List[str] = []
    validation_mode: ConfigServiceMode = ConfigServiceMode.NON_BLOCKING
    default_configs: List[Configuration] = []
    modes: Dict[str, Dict[str, str]] = {}

    def data(self) -> Dict[str, Any]:
        # pkg root path is one level up from the emews package
        # PYTHONPATH no longer required, eMews called as a module
        emews_pkg_path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
        return {
            'emews_pkg_path': emews_pkg_path,
        }


class EmewsNodeHost(ConfigService):
    """eMews Host Node."""

    name: str = "HostNode"
    group: str = GROUP_NAME
    directories: List[str] = []
    files: List[str] = ["emews_node_host.sh"]
    executables: List[str] = ["python3"]
    dependencies: List[str] = []
    startup: List[str] = ["sh emews_node_host.sh"]
    validate: List[str] = []
    shutdown: List[str] = []
    validation_mode: ConfigServiceMode = ConfigServiceMode.NON_BLOCKING
    default_configs: List[Configuration] = []
    modes: Dict[str, Dict[str, str]] = {}

    def data(self) -> Dict[str, Any]:
        # pkg root path is one level up from the emews package
        # PYTHONPATH no longer required, eMews called as a module
        emews_pkg_path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
        return {
            'emews_pkg_path': emews_pkg_path,
        }


class EmewsNodeMonitor(ConfigService):
    """eMews Monitor Node."""

    name: str = "MonitorNode"
    group: str = GROUP_NAME
    directories: List[str] = []
    files: List[str] = ["emews_node_monitor.sh"]
    executables: List[str] = ["python3"]
    dependencies: List[str] = []
    startup: List[str] = ["sh emews_node_monitor.sh"]
    validate: List[str] = []
    shutdown: List[str] = []
    validation_mode: ConfigServiceMode = ConfigServiceMode.NON_BLOCKING
    default_configs: List[Configuration] = [
        ConfigString(id="emews_start_delay", label="Start Delay", default="2"),
    ]
    modes: Dict[str, Dict[str, str]] = {}

    def data(self) -> Dict[str, Any]:
        # pkg root path is one level up from the emews package
        # PYTHONPATH no longer required, eMews called as a module
        emews_pkg_path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
        return {
            'emews_pkg_path': emews_pkg_path,
        }

