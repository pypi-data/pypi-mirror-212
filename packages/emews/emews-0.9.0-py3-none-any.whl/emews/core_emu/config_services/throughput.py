"""eMews service CORE interface."""
from typing import Any, Dict, List

import pathlib

from core.config import Configuration, ConfigString
from core.configservice.base import ConfigService, ConfigServiceMode

SERVICE_NAME: str = "throughput"
SERVICE_DISPLAY_NAME: str = "Throughput"


class EmewsServiceThroughput(ConfigService):
    """eMews service class template.  CORE 8 ConfigService paradigm."""

    name: str = SERVICE_DISPLAY_NAME
    group: str = "eMews"
    directories: List[str] = []
    files: List[str] = [f"emews_service_{SERVICE_NAME}.sh"]
    executables: List[str] = ["python3"]
    dependencies: List[str] = ["HostNode"]
    startup: List[str] = [f"sh emews_service_{SERVICE_NAME}.sh"]
    validate: List[str] = []
    shutdown: List[str] = []
    validation_mode: ConfigServiceMode = ConfigServiceMode.NON_BLOCKING
    default_configs: List[Configuration] = [
        ConfigString(id="emews_service_config", label="Service Configuration",
                     options=["default"], default="default"),
    ]
    modes: Dict[str, Dict[str, str]] = {}

    def data(self) -> Dict[str, Any]:
        emews_pkg_path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
        return {
            'emews_pkg_path': emews_pkg_path,
            'emews_service_name': SERVICE_NAME,
        }

    def get_text_template(self, name: str) -> str:
        assert name == f"emews_service_{SERVICE_NAME}.sh"
        return """
        #!/bin/sh
        export PYTHONPATH=${emews_pkg_path}
        python3 -m emews -n ${node.name} servspawn ${emews_service_name} ${config['emews_service_config']} 1>> emews_servspawn.log 2>&1
        """
