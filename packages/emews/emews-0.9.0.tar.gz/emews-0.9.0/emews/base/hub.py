"""Hub node."""
from typing import Callable, Dict, List, Mapping, Set, Tuple, Union

from enum import Enum, auto
import importlib
import inspect
import logging
import os
import pickle
import struct
import time

import psutil

from emews import __version__, _documentation_url
from emews.base.config import get_services_path, get_service_class_name, parse_service_config, parse
from emews.base.env import EnvManager
from emews.base.node import InboundEvent, ConnectionEvent, ConnectionState, NetProtocolID, NetworkHandlerError,\
    NetworkRequestError, log_record_make_pickle, NodeBase, PeerResponseError, PollEventError, SendRequestCB,\
    TimerEvent, TimerEventCB, TYPE_LEN, NET_CATEGORY_RESPONSE, NODE_ID_HUB, NODE_TYPE_HOST, NODE_TYPE_HOSTPROC,\
    NODE_TYPE_HUB, NODE_TYPE_HUBCONSOLE, NODE_TYPE_HUBMON, NAME_STR_NODE_TYPE, STR_ENCODING, NET_PROTOCOL
from emews.base.service import Service


class ConsoleCommandError(Exception):
    """Raised when a console command or group arg process method encounters an issue."""
    pass


class HubLogNetHandler(logging.Handler):
    """Logging handler for sending hub log messages on a network."""

    def __init__(self, node_name: str, log_send_cb: Callable[[bytes, int, int, bytes], None]):
        """Constructor."""
        super().__init__()
        self._hub_node_name = bytes(node_name, STR_ENCODING)
        self._log_send_cb = log_send_cb

    def emit(self, record):
        """Emit a log record."""
        pickled_log = log_record_make_pickle(record, self.format)
        self._log_send_cb(self._hub_node_name, NODE_ID_HUB, record.levelno, pickled_log)


class HubConnectionEvent(ConnectionEvent):
    """Connection event from the hub."""

    def on_recv_data(self) -> int:
        """Process data read by socket."""
        try:
            exp_bytes = super().on_recv_data()
        except NetworkRequestError as ex:
            self.logger.error(ex)
            # NACK fmt: LHHL (total_len + net_category=RESPONSE + protocol_id=0 + req_num)
            struct_fmt = ">LHHL"  # no payload in NACK
            tot_len = TYPE_LEN['H'] + TYPE_LEN['H'] + TYPE_LEN['L']
            self.write_data(struct.pack(struct_fmt, tot_len, NET_CATEGORY_RESPONSE, 0, ex.req_num))

            self._awaiting = True
            exp_bytes = ConnectionEvent.BYTES_INCOMING_REQUEST
        except PeerResponseError as ex:
            # the hub node should not get PeerResponse errors, most likely a bug
            self.logger.warning(ex)
            raise PollEventError("NACK response received") from ex

        return exp_bytes


class NodeData(ConnectionState):
    """Node related data."""

    __slots__ = ('peer_node_name', 'service_instances', 'rtt', 'hb_timer', 'hb_missed', 'is_responsive',
                 '_add_active_cb', '_del_active_cb')

    def __init__(self, peer_node_name: str, peer_node_id: int, peer_node_type: int, peer_address: str,
                 add_active_cb: Callable[['NodeData'], None],
                 del_active_cb: Callable[['NodeData'], None]):
        """Constructor."""
        super().__init__(peer_node_id, peer_node_type, peer_address)
        self.peer_node_name = peer_node_name
        self.service_instances: Set['ServiceData.ServiceInstance'] = set()
        self._add_active_cb = add_active_cb
        self._del_active_cb = del_active_cb
        self.rtt = 0  # most recent RTT
        self.hb_timer: Union[TimerEvent, None] = None  # heartbeat timer
        self.hb_missed = False  # if True, most recent heartbeat was not ACKed before timeout
        self.is_responsive = True  # is this node responding to heartbeats?

    def assign_event(self, conn_event: ConnectionEvent) -> None:
        """Assign ConnectionEvent."""
        super().assign_event(conn_event)
        self._add_active_cb(self)

        self.hb_missed = False
        self.is_responsive = True

    def unassign_event(self) -> None:
        """Unassign currently assigned ConnectionEvent."""
        super().unassign_event()
        self._del_active_cb(self)


class ServiceStatus(Enum):
    """Enums for service status."""
    INIT = auto()
    READY = auto()
    RUNNING = auto()
    FAILED = auto()
    EXIT = auto()


class ServiceData:
    """Service related data."""

    class ServiceConfig:
        """Configuration of a service."""

        __slots__ = ('config_name', 'service_class', 'send_to', 'receive_from')

        def __init__(self, config_name: str, service_class: 'ServiceData.ServiceClass'):
            """Constructor."""
            self.config_name = config_name
            self.service_class = service_class
            self.send_to: Set[ServiceData.ServiceClass] = set()
            self.receive_from: Set[ServiceData.ServiceClass] = set()

    class ServiceClass:
        """Service class data."""

        __slots__ = ('service_module', 'service_class_name', 'node_instances', 'service_instances')

        def __init__(self, service_module: 'ServiceData', service_class_name: str):
            """Constructor."""
            self.service_module = service_module
            self.service_class_name = service_class_name
            self.node_instances: Set[NodeData] = set()  # nodes that requested at least one instance
            self.service_instances: Set[ServiceData.ServiceInstance] = set()

    class ServiceInstance:
        """Service instance data"""

        __slots__ = ('service_config', 'node_instance', 'service_id', 'status')

        def __init__(self, service_config: 'ServiceData.ServiceConfig', node_instance: NodeData,
                     service_id: int):
            """Constructor."""
            self.service_config = service_config  # service config data
            self.node_instance = node_instance  # node which requested this instance
            self.service_id = service_id  # service instance id
            self.status = ServiceStatus.INIT

        @property
        def service_class(self) -> 'ServiceData.ServiceClass':
            """Return this service instance's class."""
            return self.service_config.service_class

        @property
        def service_module(self) -> 'ServiceData':
            """Return this service instance's module."""
            return self.service_class.service_module

        @property
        def service_display_name(self) -> str:
            """Return the display name of the service module that this instance belongs."""
            return self.service_module.service_display_name

        @property
        def full_name(self) -> str:
            """Return the full name of this service (service.config)."""
            return f"{self.service_display_name}.{self.service_config.config_name}"

    __slots__ = ('service_name', 'service_display_name', 'service_classes', 'service_configs')

    def __init__(self, service_name: str, service_display_name: str):
        """Constructor."""
        self.service_name = service_name  # service dir name
        self.service_display_name = service_display_name  # display name of service, as given in default.yml
        self.service_classes: Dict[str, ServiceData.ServiceClass] = {}  # key=class name
        self.service_configs: Dict[str, ServiceData.ServiceConfig] = {}  # key=config filename


class NetState:
    """Global network state."""

    __slots__ = ('node_by_id', 'node_by_name', 'service_by_name', 'service_by_id',
                 'active_nodes', 'active_hosts', 'active_consoles', 'active_monitors', 'active_receivers',
                 'active_node_by_type', '_free_node_id', '_free_service_instance_id',
                 'scn_autostart', '_scn_running', 'scn_autostart_delay', 'scn_duration',
                 '_scn_run_start_ts', '_scn_run_stop_ts', '_scn_warnings_offset', '_scn_errors_offset',
                 '_scn_warnings_tot', '_scn_errors_tot', 'log_warnings', 'log_errors')

    def __init__(self, scn_autostart: bool, delay_scn_start: int, duration_scn: int):
        """Constructor."""

        if scn_autostart:
            self.scn_autostart = True
        else:
            self.scn_autostart = False  # when True, exp scenario will automatically start

        if delay_scn_start is not None and delay_scn_start > 0:
            self.scn_autostart_delay = delay_scn_start
        else:
            self.scn_autostart_delay = 0  # interval (seconds) to wait before starting scn if autostart

        if duration_scn is not None and duration_scn > 0:
            self.scn_duration = duration_scn
        else:
            self.scn_duration = 0  # interval (seconds) of scenario duration (0 = no expiry, unlimited)

        self.service_by_name: Dict[str, ServiceData] = {}  # service module data
        self.service_by_id: Dict[int, ServiceData.ServiceInstance] = {}

        self.node_by_id: Dict[int, NodeData] = {}
        self.node_by_name: Dict[str, NodeData] = {}

        # nodes that are currently connected, by type
        self.active_nodes: Set[NodeData] = set()
        self.active_hosts: Set[NodeData] = set()
        self.active_consoles: Set[NodeData] = set()
        self.active_monitors: Set[NodeData] = set()

        # service instances which are active, lookup by service class that can send data to them
        self.active_receivers: Dict[ServiceData.ServiceClass, Set[ServiceData.ServiceInstance]] = {}

        self.active_node_by_type: Dict[int, Set[NodeData]] = {
            NODE_TYPE_HOST: self.active_hosts,
            NODE_TYPE_HUBCONSOLE: self.active_consoles,
            NODE_TYPE_HUBMON: self.active_monitors,
        }

        self._free_node_id: int = NODE_ID_HUB + 1
        self._free_service_instance_id: int = 1

        # experiment scenario status
        self._scn_run_start_ts = None  # timestamp of start time of experiment scenario
        self._scn_run_stop_ts = None  # timestamp of stop time of experiment scenario
        self._scn_running = False  # true when an exp scenario is running
        self._scn_warnings_offset = 0  # warning loglevel count at start of scenario
        self._scn_errors_offset = 0  # error loglevel count at start of scenario
        self._scn_warnings_tot = 0  # warning loglevel count during scenario
        self._scn_errors_tot = 0  # error loglevel count during scenario

        self.log_warnings = 0  # current count of log warnings
        self.log_errors = 0  # current count of log errors

    def scn_start(self) -> None:
        """Start the experiment scenario."""
        assert self._scn_run_start_ts is None

        self._scn_warnings_offset = self.log_warnings
        self._scn_errors_offset = self.log_errors

        self._scn_run_start_ts = time.monotonic()
        self._scn_running = True

    def scn_stop(self) -> None:
        """Stop the experiment scenario."""
        assert self._scn_running

        # final scenario loglevel counts
        self._scn_warnings_tot = self.log_warnings - self._scn_warnings_offset
        self._scn_errors_tot = self.log_errors - self._scn_errors_offset

        self._scn_run_stop_ts = time.monotonic()
        self._scn_running = False

    @property
    def scn_running(self) -> bool:
        """Return true if experiment scenario is currently running."""
        return self._scn_running

    @property
    def scn_started(self) -> bool:
        """Return true if experiment scenario is running/has already run."""
        return self._scn_run_start_ts is not None

    def scn_status(self) -> Tuple[float, str, int, int]:
        """
        Return the current status of the experiment scenario as a
        tuple(elapsed_time, scn_status, warning_counts, error_counts).
        """
        if self._scn_running:
            assert self._scn_run_start_ts is not None
            warning_counts = self.log_warnings - self._scn_warnings_offset
            error_counts = self.log_errors - self._scn_errors_offset
            elapsed_time = time.monotonic() - self._scn_run_start_ts
        elif self.scn_started:
            assert not self._scn_running
            assert self._scn_run_stop_ts is not None
            warning_counts = self._scn_warnings_tot
            error_counts = self._scn_errors_tot
            elapsed_time = self._scn_run_stop_ts - self._scn_run_start_ts
        else:
            # do not count warnings/errors before scenario starts
            assert not self._scn_running
            assert self._scn_run_start_ts is None
            warning_counts = 0
            error_counts = 0
            elapsed_time = 0.0

        if error_counts > 0:
            scn_status = 'RED'
        elif warning_counts > 0:
            scn_status = 'YELLOW'
        else:
            scn_status = 'GREEN'

        return elapsed_time, scn_status, warning_counts, error_counts

    def is_responsive(self, node_id: int) -> bool:
        """Return whether the node given by id is responding to heartbeats."""
        return self.node_by_id[node_id].is_responsive

    def new_service_instance(self, service_name: str, service_config_filename: str,
                             node_data: NodeData) -> ServiceData.ServiceInstance:
        """Add a new service instance to node.  Returns ServiceInstance."""
        try:
            service_data = self.service_by_name[service_name]
        except KeyError:
            raise NetworkHandlerError(f"service '{service_name}' does not exist")

        service_config_data = service_data.service_configs.get(service_config_filename)

        if service_config_data is None:
            # configuration not previously loaded
            try:
                service_config = parse_service_config(service_name, service_config_filename)
            except OSError as ex:
                raise NetworkHandlerError(f"service configuration for service '{service_name}' "
                                          f"could not be loaded: {ex}") from ex

            service_class_str = get_service_class_name(service_config)

            try:
                service_class_data = service_data.service_classes[service_class_str]
            except KeyError:
                raise NetworkHandlerError(f"in {service_config_filename}: service class '{service_class_str}' for "
                                          f"service '{service_name}' does not exist")

            service_config_data = ServiceData.ServiceConfig(service_config_filename, service_class_data)

            for send_class_name in service_config.get("send_to", []):
                # service classes which these service instances can send messages to
                try:
                    send_class_data = service_data.service_classes[send_class_name]
                except KeyError:
                    raise NetworkHandlerError(f"in {service_config_filename}: send_to service class "
                                              f"'{send_class_name}' for service '{service_name}' does not exist")

                service_config_data.send_to.add(send_class_data)

            for recv_class_name in service_config.get("receive_from", []):
                # service classes which these service instances can receive messages from
                try:
                    recv_class_data = service_data.service_classes[recv_class_name]
                except KeyError:
                    raise NetworkHandlerError(f"in {service_config_filename}: receive_from service class "
                                              f"'{recv_class_name}' for service '{service_name}' does not exist")

                service_config_data.receive_from.add(recv_class_data)
        else:
            # service config data for this configuration already exists, use it
            service_class_data = service_config_data.service_class

        new_service_id = self._free_service_instance_id
        self._free_service_instance_id += 1

        service_instance_data = ServiceData.ServiceInstance(service_config_data, node_data, new_service_id)

        node_data.service_instances.add(service_instance_data)
        service_class_data.service_instances.add(service_instance_data)

        service_class_data.node_instances.add(node_data)

        self.service_by_id[new_service_id] = service_instance_data

        return service_instance_data

    def new_node_instance(self, peer_node_name: str, peer_node_type: int, peer_address: str) -> NodeData:
        """Add a new node to the repo.  Returns NodeData."""
        new_node_id = self._free_node_id
        self._free_node_id += 1

        node_data = NodeData(peer_node_name, new_node_id, peer_node_type, peer_address,
                             self._add_active, self._del_active)

        self.node_by_id[node_data.peer_node_id] = node_data
        self.node_by_name[node_data.peer_node_name] = node_data

        return node_data

    def _add_active(self, node_data: NodeData) -> None:
        """Add NodeData to appropriate active set."""
        self.active_nodes.add(node_data)
        active_set = self.active_node_by_type.get(node_data.peer_node_type)
        if active_set is not None:
            active_set.add(node_data)

    def _del_active(self, node_data: NodeData) -> None:
        """Remove NodeData from appropriate active set."""
        self.active_nodes.remove(node_data)
        active_set = self.active_node_by_type.get(node_data.peer_node_type)
        if active_set is not None:
            active_set.remove(node_data)

    def parse_services(self, logger: logging.Logger) -> None:
        """Get service listing and create service data."""
        with os.scandir(get_services_path()) as it_service_root:
            for entry_service_root in it_service_root:
                if not entry_service_root.name.startswith('.') and entry_service_root.is_dir():
                    # may be a service directory
                    service_name: str = entry_service_root.name

                    with os.scandir(entry_service_root.path) as it_dir:
                        # check if contents are consistent with a service
                        service_module = None
                        default_config = None
                        for entry_dir in it_dir:
                            if entry_dir.is_file():
                                if entry_dir.name == 'service.py':
                                    try:
                                        service_module = importlib.import_module(
                                            f"emews.services.{service_name}.service")
                                    except ImportError as ex:
                                        # apparently not a module
                                        logger.warning("While parsing services: directory '%s' contains service.py"
                                                       " but cannot be imported: %s", service_name, ex)
                                        break
                                elif entry_dir.name == 'default.yml':
                                    try:
                                        default_config = parse(entry_dir.path)
                                    except Exception as ex:
                                        # apparently not a YAML file
                                        logger.warning("While parsing services: directory '%s' contains default.yml"
                                                       " but cannot be loaded: %s", service_name, ex)
                                        break

                        if service_module is not None:
                            if default_config is None:
                                logger.warning("While parsing services: directory '%s' contains service.py"
                                               " but is missing default.yml configuration", service_name)
                                continue

                            # get all service classes in the module
                            service_classes: Set[str] = set()
                            for name, obj in inspect.getmembers(service_module):
                                if inspect.isclass(obj) and issubclass(obj, Service) and obj != Service:
                                    # service class (child of Service)
                                    service_classes.add(name)

                            if 'DefaultService' not in service_classes:
                                logger.warning("While parsing services: for service '%s', default service "
                                               "class 'DefaultService' not found", service_name)
                                continue

                            service_display_name = default_config.get('display_name')

                            if service_display_name is None:
                                service_display_name = service_name

                            # valid service - everything present
                            service_data = ServiceData(service_name, service_display_name)
                            self.service_by_name[service_name] = service_data

                            for service_class_name in service_classes:
                                service_class_instance = ServiceData.ServiceClass(service_data, service_class_name)
                                service_data.service_classes[service_class_name] = service_class_instance

                                self.active_receivers[service_class_instance] = set()

        service_names = []
        for service_data in self.service_by_name.values():
            for service_cls_str in service_data.service_classes.keys():
                service_names.append(f"{service_data.service_display_name}.{service_cls_str}")

        if len(service_names):
            logger.info("%d services are available: %s", len(service_names), ', '.join(service_names))
        else:
            logger.warning("No services available")


# console command skeleton
CONSOLE_CMD = {
    'exit': {
        'cmd_class': 'NonHubConsoleCommand',
        'cmd_help': "Exit the console session.",
    },
    'exp': {
        'cmd_help': "Commands that apply to the experiment scenario.",
        'grp_subcmd': {
            'status': {
                'cmd_help': "Return current status of the experiment scenario.",
            },
            'set_duration': {
                'cmd_help': "Set the duration of the experiment scenario, providing it has not started already "
                            "(0 = unlimited duration).",
                'cmd_arg': {
                    'duration': {
                        'arg_type': int,
                        'arg_help': "length of time (seconds) in which the experiment scenario should run",
                    },
                },
            },
            'start': {
                'cmd_help': "Start the experiment scenario, if it is currently not running, and has never been run.",
            },
            'stop': {
                'cmd_help': "Stop the experiment scenario, if it is currently running.  "
                            "Note that even if a duration is set, a running scenario will still stop.  "
                            "Once a scenario is stopped, it cannot be restarted.",
            },
        },
    },
    'help': {
        'cmd_class': 'HelpConsoleCommand',
        'cmd_help': "Get help on a specific command.  Type 'list commands' to get a listing of all "
                    "available commands.",
    },
    'history': {
        'cmd_help': "Return command history among all console nodes.",
    },
    'list': {
        'cmd_help': "Return a listing based on the command given.",
        'grp_subcmd': {
            'commands': {
                'cmd_help': "Return a listing of available console commands.",
            },
            'env_keys': {
                'cmd_help': "Return a listing of available network environment keys.",
            },
            'envs': {
                'cmd_help': "Return a listing of loaded network environments.",
            },
            'nodes': {
                'cmd_help': "Return a listing of currently running nodes.",
            },
            'services': {
                'cmd_help': "Return a listing of registered service instances.",
            },
        },
    },
    'node': {
        'cmd_help': "Commands that apply to nodes.",
        'grp_arg': {
            'arg_name': 'node_id',
            'arg_type': int,
            'arg_help': "id of node to apply command",
        },
        'grp_subcmd': {
            'info': {
                'cmd_help': "Return information about the given node.",
            },
            'spawn': {
                'cmd_help': "Spawn a new service instance on the given node.",
                'cmd_arg_default': 'default',
                'cmd_arg': {
                    'service_name': {
                        'arg_type': str,
                        'arg_help': "name of service to spawn",
                    },
                    'config_filename': {
                        'arg_type': str,
                        'arg_help': "filename of the service configuration to load",
                    },
                },
            },
        },
    },
    'service': {
        'cmd_help': "Commands that apply to service instances.",
        'grp_arg': {
            'arg_name': 'service_id',
            'arg_type': int,
            'arg_help': "id of service instance to apply command",
        },
        'grp_subcmd': {
            'info': {
                'cmd_help': "Display information about the service instance.",
            },
            'start': {
                'cmd_help': "Start the given service instance.",
            },
            'stop': {
                'cmd_help': "Stop the given service instance.",
            },
        },
    },
    'uptime': {
        'cmd_help': "Display uptime information of the Hub node.",
    },
    'usage': {
        'cmd_help': "Resource usage information.",
        'grp_subcmd': {
            'process': {
                'cmd_help': "Resource usage information of the Hub node's process.",
            },
            'system': {
                'cmd_help': "Resource usage information of the system the Hub node is running on.",
            },
        },
    },
    'version': {
        'cmd_help': "Display eMews version, as reported by the Hub node.",
    },
}


class ConsoleCommand:
    """A console command."""

    __slots__ = ('_cmd_cb', '_arg_names', '_arg_cast', '_arg_default')

    def __init__(self, command_cb: Union[Callable[..., str], None],
                 args_lst: List[Tuple[Union[int, float, str], str]],
                 default_arg_val: Union[str, None] = None):
        """Constructor."""
        self._cmd_cb = command_cb

        arg_names_lst = []
        arg_cast_lst = []
        for arg_def in args_lst:
            arg_names_lst.append(arg_def[1])
            if arg_def[0] == int:
                arg_cast_lst.append(ConsoleCommand.arg_cast_int)
            elif arg_def[0] == float:
                arg_cast_lst.append(ConsoleCommand.arg_cast_float)
            else:
                # assume string type
                arg_cast_lst.append(ConsoleCommand.arg_no_cast)

        self._arg_names = arg_names_lst
        self._arg_cast = arg_cast_lst
        self._arg_default = default_arg_val

    @staticmethod
    def arg_cast_int(cmd_arg: str) -> int:
        """Cast an arg to an int."""
        try:
            parsed_arg = int(cmd_arg)
        except ValueError:
            raise ValueError("cannot be cast to int")

        return parsed_arg

    @staticmethod
    def arg_cast_float(cmd_arg: str) -> float:
        """Cast an arg to a float."""
        try:
            parsed_arg = float(cmd_arg)
        except ValueError:
            raise ValueError("cannot be cast to float")

        return parsed_arg

    @staticmethod
    def arg_no_cast(cmd_arg: str) -> str:
        """Do not cast (arg is a str)."""
        return cmd_arg

    def process_command(self, cmd_name: str, group_objs: List, cmd_args: List[str]) -> str:
        """Process the command with args."""
        if len(cmd_args) < len(self._arg_names) and self._arg_default is not None:
            # append the default arg
            cmd_args.append(self._arg_default)

        if len(cmd_args) != len(self._arg_names):
            if not len(self._arg_names):
                req_str = "does not take any arguments"
            elif len(self._arg_names) == 1:
                req_str = "requires 1 argument"
            else:
                if self._arg_default is not None:
                    req_str = f"requires {len(self._arg_names) - 1} or {len(self._arg_names)} arguments " \
                              "(last argument has a default value and is optional)"
                else:
                    req_str = f"requires {len(self._arg_names)} arguments"

            if self._arg_default is not None:
                # remove default arg value to keep count consistent
                del cmd_args[-1]

            if len(cmd_args) == 1:
                giv_str = "1 was"
            else:
                giv_str = f"{len(cmd_args)} were"

            return f"{cmd_name}: command {req_str}, but {giv_str} given"

        parsed_args = []
        for arg_name, arg_cast, cmd_arg in zip(self._arg_names, self._arg_cast, cmd_args):
            try:
                parsed_arg = arg_cast(cmd_arg)
            except ValueError as ex:
                return f"{cmd_name}: argument <{arg_name}> {ex}: {cmd_arg}"

            parsed_args.append(parsed_arg)

        try:
            ret_str = self._cmd_cb(*group_objs, *parsed_args)
        except ConsoleCommandError as ex:
            return f"{cmd_name}: {ex}"

        return ret_str


class HelpConsoleCommand(ConsoleCommand):
    """The help command."""

    __slots__ = ('type_str',)

    def __init__(self):
        """Constructor."""
        super().__init__(None, [])
        self.type_str = {
            str: 'string',
            int: 'integer',
            float: 'float'
        }

    def process_command(self, cmd_name: str, group_objs: List, cmd_args: List[str]) -> str:
        """Return help string for given command."""
        assert cmd_name == 'help'

        if not len(cmd_args):
            # help given without any command, return help string for 'help' itself
            cmd_args.append(cmd_name)

        cmd_chain = []
        current_cmd = CONSOLE_CMD
        cmd_str = ''
        cmd_arg_desc = []
        grp_arg_desc = []
        grp_skel = None

        for cmd_str in cmd_args:
            cmd_chain.append(cmd_str)

            try:
                current_cmd = current_cmd[cmd_str]
            except KeyError:
                cmd_str = f"Command '{cmd_str}' cannot be found."
                break

            grp_skel: Union[dict, None] = current_cmd.get('grp_subcmd')
            if grp_skel is None:
                # this is the command (no CommandGroup)
                cmd_str = current_cmd['cmd_help']
                cmd_arg_dct = current_cmd.get('cmd_arg', {})
                cmd_arg_default = current_cmd.get('cmd_arg_default')

                # get any cmd argument descriptions
                for arg_name, arg_data in cmd_arg_dct.items():
                    cmd_arg_desc.append(f"- {arg_name} ({self.type_str[arg_data['arg_type']]}): "
                                        f"{arg_data['arg_help']}.")
                    cmd_chain.append(f"<{arg_name}>")

                if len(cmd_arg_dct) and cmd_arg_default is not None:
                    cmd_arg_desc.append(f"  - default value: '{cmd_arg_default}'")

                break

            # CommandGroup
            cmd_str = current_cmd['cmd_help']  # set to group help, in case no sub-cmd given
            # get any group arg descriptions
            grp_arg_skel: Union[dict, None] = current_cmd.get('grp_arg')
            if grp_arg_skel is not None:
                grp_arg_name = grp_arg_skel['arg_name']
                grp_arg_desc.append(
                    f"- {grp_arg_name} ({self.type_str[grp_arg_skel['arg_type']]}): "
                    f"{grp_arg_skel['arg_help']}.")
                cmd_chain.append(f"<{grp_arg_name}>")

            # set current cmd to the group skel, which contains the sub-commands
            current_cmd = grp_skel

        if len(grp_arg_desc):
            str_join = '\n'.join(grp_arg_desc)
            grp_arg_str = f"Prerequisite Arguments:\n{str_join}\n\n"
        else:
            grp_arg_str = ''

        if len(cmd_arg_desc):
            str_join = '\n'.join(cmd_arg_desc)
            cmd_arg_str = f"\n\nCommand Arguments:\n{str_join}"
        elif grp_skel is not None:
            # help for a command group was given without a sub-command, fill in the commands
            cmd_chain.append("<command>")
            cmd_arg_desc.append("\n\nAvailable Commands:")
            for cmd_name, cmd_data in grp_skel.items():
                cmd_arg_desc.append(f"- {cmd_name}: {cmd_data['cmd_help']}")
            cmd_arg_str = '\n'.join(cmd_arg_desc)
        else:
            # command given, but it has no args
            cmd_arg_str = ''

        return f"{' '.join(cmd_chain)}\n\n{grp_arg_str}{cmd_str}{cmd_arg_str}"


class NonHubConsoleCommand(ConsoleCommand):
    """A command which is handled on the client side."""

    __slots__ = ()

    def __init__(self):
        """Constructor."""
        super().__init__(None, [])

    def process_command(self, cmd_name: str, group_objs: List, cmd_args: List[str]) -> str:
        """Return string stating that this command should not be executed on the hub."""
        return f"The command '{cmd_name}' is processed on the client side, but was passed to the " \
               f"Hub for processing.  This may be a bug."


class ConsoleCommandGroup:
    """A console command group: command in which the argument is a sub-command."""

    __slots__ = ('_commands', '_group_arg_name', '_group_arg_cast', '_group_arg_process')

    def __init__(self, command_dct: Dict[str, Union['ConsoleCommandGroup', ConsoleCommand]],
                 group_arg: Union[Tuple[Union[int, str], str, Callable], None] = None):
        """Constructor."""
        self._commands = command_dct
        if group_arg is not None:
            self._group_arg_name = group_arg[1]
            self._group_arg_process = group_arg[2]
            if group_arg[0] == int:
                self._group_arg_cast = ConsoleCommand.arg_cast_int
            elif group_arg[0] == str:
                self._group_arg_cast = ConsoleCommand.arg_no_cast
        else:
            self._group_arg_name = None
            self._group_arg_process = None
            self._group_arg_cast = None

    def process_command(self, cmd_name: str, group_objs: List, cmd_args: List[str]) -> str:
        """Process the command and subcommand."""
        if not len(cmd_args):
            if self._group_arg_cast is None:
                return f"{cmd_name}: requires 1 argument (<command>), but 0 were given\n" \
                       f"command choices: {', '.join(self._commands.keys())}"

            return f"{cmd_name}: requires 2 arguments (<{self._group_arg_name}> and " \
                   "<command>), but 0 were given\n" \
                   f"command choices: {', '.join(self._commands.keys())}"

        if self._group_arg_cast is not None:
            # group arg present
            if len(cmd_args) == 1:
                # check if the arg is a sub-command
                if cmd_args[0] in self._commands:
                    return f"{cmd_name}: missing argument <{self._group_arg_name}> before " \
                           f"command '{cmd_args[0]}'"

                return f"{cmd_name}: requires 2 arguments (<{self._group_arg_name}> and " \
                       "<command>), but 1 was given\n" \
                       f"command choices: {', '.join(self._commands.keys())}"

            try:
                parsed_group_arg = self._group_arg_cast(cmd_args[0])
            except ValueError as ex:
                return f"{cmd_name}: argument <{self._group_arg_name}> {ex}: {cmd_args[0]}"

            try:
                group_objs.append(self._group_arg_process(parsed_group_arg))
            except ConsoleCommandError as ex:
                return f"{cmd_name}: {ex}"

            cmd_args.pop(0)

        sub_cmd = cmd_args.pop(0)  # arg len expected to be small

        try:
            cmd_obj = self._commands[sub_cmd]
        except KeyError:
            return f"{cmd_name}: command '{sub_cmd}' not found " \
                   f"(choices: {', '.join(self._commands.keys())})"

        return cmd_obj.process_command(f"{cmd_name} {sub_cmd}", group_objs, cmd_args)


class ConsoleManager:
    """Manages hub console command processing and node/system stats."""

    __slots__ = ('logger_dist', '_ns', '_env', '_p_info', '_start_time', '_consoles',
                 '_console_commands', '_last_console_connection', '_command_history',
                 '_cb_send_request', '_cb_scn_start', '_cb_scn_stop')

    def __init__(self, logger_dist: logging.Logger, ns: NetState, env_manager: EnvManager,
                 send_request_cb: SendRequestCB, scn_start_cb: Callable[[], None], scn_stop_cb: Callable[[], None]):
        """Constructor."""
        self.logger_dist = logger_dist
        self._ns: NetState = ns
        self._env: EnvManager = env_manager
        self._cb_send_request = send_request_cb
        self._cb_scn_start = scn_start_cb
        self._cb_scn_stop = scn_stop_cb

        self._p_info = psutil.Process()  # information about this process
        self._p_info.cpu_percent(interval=None)  # prime the CPU usage
        psutil.cpu_percent(interval=None)

        self._start_time: float = 0.0  # timestamp when node starts

        self._console_commands: Dict[str, Union[ConsoleCommand, ConsoleCommandGroup]] = \
            self._init_commands("", CONSOLE_CMD)

        self._consoles: Dict[int, NodeData] = {}  # HubConsole nodes
        self._last_console_connection: Union[float, None] = None
        self._command_history = []  # history of console commands

    def _init_commands(self, cmd_chain: str, cmd_skel: dict) -> dict:
        """Build console commands recursively."""
        cmd_dct = {}
        for cmd_name, cmd_data in cmd_skel.items():
            cmd_class = cmd_data.get('cmd_class')
            if cmd_class is not None:
                # this is a command with a custom class
                cmd_dct[cmd_name] = globals()[cmd_class]()  # module level dict of goodies
                continue

            grp_skel: dict = cmd_data.get('grp_subcmd')
            if grp_skel is not None:
                # this is a CommandGroup
                grp_arg_skel = cmd_data.get('grp_arg')
                if grp_arg_skel is not None:
                    # currently allow 1 group arg
                    grp_arg = (grp_arg_skel['arg_type'], grp_arg_skel['arg_name'],
                               getattr(self, f"_cg_{cmd_chain}{cmd_name}"))
                else:
                    grp_arg = None

                cmd_dct[cmd_name] = ConsoleCommandGroup(
                    self._init_commands(f"{cmd_chain}{cmd_name}_", grp_skel), group_arg=grp_arg)
                continue

            # ConsoleCommand
            cmd_arg = []
            cmd_arg_default = None
            cmd_arg_skel: dict = cmd_data.get('cmd_arg')
            if cmd_arg_skel is not None:
                for cmd_arg_name, cmd_arg_data in cmd_arg_skel.items():
                    cmd_arg.append((cmd_arg_data['arg_type'], cmd_arg_name))
                # check for default arg val here, because this should be None if there are no args
                cmd_arg_default = cmd_data.get('cmd_arg_default')  # if exists, will be applied to last cmd_arg

            cmd_dct[cmd_name] = ConsoleCommand(getattr(self, f"_cc_{cmd_chain}{cmd_name}"), cmd_arg,
                                               default_arg_val=cmd_arg_default)

        return cmd_dct

    def start(self):
        """Start the console manager."""
        self._start_time = time.monotonic()  # reference start time

    def welcome_msg(self, node_name: str) -> str:
        """Generate and return welcome message."""
        welcome_msg = f"Welcome to eMews Hub '{node_name}'\n\n" \
                      f"  * Documentation: {_documentation_url}\n\n" \
                      f"  Currently connected console nodes: {len(self._ns.active_consoles)}\n" \
                      f"  Currently connected monitor nodes: {len(self._ns.active_monitors)}\n\n" \
                      f"  System CPU usage: {psutil.cpu_percent(interval=None):.1f}%\n" \
                      f"  System MEM usage: {psutil.virtual_memory().percent:.1f}%"

        if self._last_console_connection is not None:
            last_connection = time.ctime(self._last_console_connection)
            welcome_msg = f"{welcome_msg}\n\n  Last console node connection: {last_connection}"

        self._last_console_connection = time.time()

        return welcome_msg

    @staticmethod
    def format_duration(duration: float) -> str:
        """Return string representing a time interval from start_ts to current time."""
        dur_t = time.gmtime(duration)

        if dur_t.tm_yday == 1:
            # up under a day (day in year starts at 1)
            up_days = ""
        elif dur_t.tm_yday == 2:
            # up one day
            up_days = "1 day, "
        else:
            up_days = f"{dur_t.tm_yday - 1} days, "

        return f"{up_days}{dur_t.tm_hour}:{dur_t.tm_min:02d}:{dur_t.tm_sec:02d}"

    # network request handlers
    def process_console_command(self, node_id: int, cmd_args: bytes) -> Tuple[bytes]:
        """Process a console command."""
        assert self._ns.node_by_id[node_id].peer_node_type == NODE_TYPE_HUBCONSOLE

        cmd_lst = cmd_args.decode().split()

        try:
            cmd_obj = self._console_commands[cmd_lst[0]]
        except KeyError:
            return bytes(f"{cmd_lst[0]}: command not found\n", STR_ENCODING),

        self._command_history.append((time.time(), node_id, ' '.join(cmd_lst)))

        ret_str = cmd_obj.process_command(cmd_lst[0], [], cmd_lst[1:])

        if len(ret_str):
            ret_str = f"{ret_str}\n"

        return bytes(ret_str, STR_ENCODING),

    @staticmethod
    def _format_list_output(col_align_lst: List[str], val_lst: List[List[str]]) -> str:
        """Format given list and return string representation."""
        col_len = [0] * len(val_lst[0])

        # calculate column spacing
        for row in val_lst:
            for idx, val_str in enumerate(row):
                if len(val_str) > col_len[idx]:
                    col_len[idx] = len(val_str)

        output_rows = []
        for row in val_lst:
            row_lst = []
            for val_len, val_str, col_align in zip(col_len, row, col_align_lst):
                row_lst.append(f"{val_str:{col_align}{val_len}.{val_len}s}")

            output_rows.append("   ".join(row_lst))

        return "\n".join(output_rows)

    # console command handlers
    def _cg_node(self, node_id: int) -> NodeData:
        """Get node data from node id."""
        try:
            node_data = self._ns.node_by_id[node_id]
        except KeyError:
            raise ConsoleCommandError(f"node with id '{node_id}' does not exist")

        return node_data

    def _cg_service(self, service_id: int) -> ServiceData.ServiceInstance:
        """Get service data from service instance id."""
        try:
            service_instance_data = self._ns.service_by_id[service_id]
        except KeyError:
            raise ConsoleCommandError(f"service instance with id '{service_id}' does not exist")

        return service_instance_data

    def _cc_node_spawn(self, node_data: NodeData, service_name: str, config_filename: str) -> str:
        """Spawn a new service instance at node."""
        if not node_data.is_connected:
            raise ConsoleCommandError(f"node {node_data.peer_node_id} is offline")

        if node_data.peer_node_type != NODE_TYPE_HOST:
            raise ConsoleCommandError(f"node {node_data.peer_node_id} is not a host")

        try:
            service_instance_data = self._ns.new_service_instance(service_name, config_filename, node_data)
        except NetworkHandlerError as ex:
            raise ConsoleCommandError(ex)

        service_id = service_instance_data.service_id

        self.logger_dist.info("New instance of service '%s' with service id %d assigned to node %d",
                              service_instance_data.full_name, service_id, node_data.peer_node_id)

        self._cb_send_request(node_data, NetProtocolID.HOST_SERVICE_SPAWN,
                              request_data=(bytes(service_name, STR_ENCODING),
                                            bytes(config_filename, STR_ENCODING),
                                            service_id,
                                            bytes(service_instance_data.service_display_name, STR_ENCODING)),
                              local_data=f"service spawn (new service id: {service_id}, "
                                         f"service name: {service_name}, configuration: {config_filename})")

        return ""

    @staticmethod
    def _cc_node_info(node_data: NodeData) -> str:
        """Display information about the node."""
        return f"node name: {node_data.peer_node_name}\nnode type: {NAME_STR_NODE_TYPE[node_data.peer_node_type]}"

    @staticmethod
    def _cc_service_info(service_instance_data: ServiceData.ServiceInstance) -> str:
        """Display information about the node."""
        service_config_data = service_instance_data.service_config

        send_classes_str = ", ".join([cls_data.service_class_name for cls_data in service_config_data.send_to])
        recv_classes_str = ", ".join([cls_data.service_class_name for cls_data in service_config_data.receive_from])

        return f"full name: {service_instance_data.full_name}\n" \
               f"config:    {service_config_data.config_name}\n" \
               f"class:     {service_config_data.service_class.service_class_name}\n" \
               f"status:    {service_instance_data.status.name}\n\n" \
               "classes configured for sending data to / receiving data from:\n" \
               f"- send: {send_classes_str}\n- recv: {recv_classes_str}"

    def _cc_service_start(self, service_instance_data: ServiceData.ServiceInstance) -> str:
        """Start a registered service."""
        node_data = service_instance_data.node_instance
        service_id = service_instance_data.service_id

        if not node_data.is_connected:
            raise ConsoleCommandError(f"node {node_data.peer_node_id} hosting this service is offline")

        if service_instance_data.status != ServiceStatus.READY:
            if service_instance_data.status == ServiceStatus.RUNNING:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) is already running")
            if service_instance_data.status == ServiceStatus.FAILED:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) has failed")
            if service_instance_data.status == ServiceStatus.EXIT:
                raise ConsoleCommandError(
                    f"service {service_id} (node {node_data.peer_node_id}) has previously terminated")
            if service_instance_data.status == ServiceStatus.INIT:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) is still initializing")

        ack_msg = f"service start (service name: {service_instance_data.full_name}, service id: {service_id})"
        self._cb_send_request(node_data, NetProtocolID.HOST_SERVICE_START,
                              request_data=(service_id,), local_data=ack_msg)

        return ""

    def _cc_service_stop(self, service_instance_data: ServiceData.ServiceInstance) -> str:
        """Stop a registered service."""
        node_data = service_instance_data.node_instance
        service_id = service_instance_data.service_id

        if not node_data.is_connected:
            raise ConsoleCommandError(f"node {node_data.peer_node_id} hosting this service is offline")

        if service_instance_data.status != ServiceStatus.RUNNING:
            if service_instance_data.status == ServiceStatus.READY:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) is not running")
            if service_instance_data.status == ServiceStatus.FAILED:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) has failed")
            if service_instance_data.status == ServiceStatus.EXIT:
                raise ConsoleCommandError(
                    f"service {service_id} (node {node_data.peer_node_id}) has previously terminated")
            if service_instance_data.status == ServiceStatus.INIT:
                raise ConsoleCommandError(f"service {service_id} (node {node_data.peer_node_id}) is still initializing")

        ack_msg = f"service stop (service name: {service_instance_data.full_name}, service id: {service_id})"
        self._cb_send_request(node_data, NetProtocolID.HOST_SERVICE_STOP,
                              request_data=(service_id,), local_data=ack_msg)

        return ""

    @staticmethod
    def _cc_version() -> str:
        """Print eMews version."""
        return f"eMews {__version__}"

    def _cc_history(self) -> str:
        """Print command history among all consoles."""
        val_lst = [["TIME", "ID", "COMMAND"]]
        for cmd_timestamp, cmd_node_id, cmd_name in self._command_history:
            val_lst.append([time.ctime(cmd_timestamp), str(cmd_node_id), cmd_name])

        return self._format_list_output(['', '>', ''], val_lst)

    def _cc_exp_set_duration(self, duration: int) -> str:
        """Set duration of experiment scenario."""
        ns = self._ns

        if ns.scn_running:
            return "Cannot set network experiment scenario duration, as it is already running"

        if ns.scn_started:
            return "Cannot set network experiment scenario duration, as it already finished, and can only be run once"

        ns.scn_duration = duration

        return ""

    def _cc_exp_status(self) -> str:
        """Return current status of experiment scenario."""
        ns = self._ns

        elapsed_time, scn_status, warning_counts, error_counts = ns.scn_status()
        status_str = f"- elapsed time: {self.format_duration(elapsed_time)}\n" \
                     f"- status: {scn_status}\n  - warnings: {warning_counts}\n  - errors:   {error_counts}"

        if ns.scn_running:
            run_str = f"Yes\n{status_str}"
        elif ns.scn_started:
            run_str = f"No (finished)\n{status_str}"
        else:
            run_str = 'No'

        if ns.scn_autostart:
            autostart_str = f"Yes (autostart delay: {ns.scn_autostart_delay})"
        else:
            autostart_str = 'No'

        if ns.scn_duration == 0:
            duration_str = 'Unlimited'
        else:
            duration_str = f"{ns.scn_duration}s"

        return f"Scenario running: {run_str}\n\nParameters:\n" \
               f"- Autostart enabled: {autostart_str}\n" \
               f"- Scenario duration: {duration_str}"

    def _cc_exp_start(self) -> str:
        """Start the experiment scenario, if it is not currently running."""
        ns = self._ns
        if ns.scn_autostart:
            return "Network experiment scenario cannot be started manually as autostart enabled"

        if ns.scn_running:
            return "Network experiment scenario is already running"

        if ns.scn_started:
            return "Network experiment scenario has already run, and can only execute the scenario once"

        self._cb_scn_start()

        if ns.scn_duration > 0:
            return f"Network experiment scenario started, will run for a duration of {ns.scn_duration} seconds"

        return "Network experiment scenario started, will run without duration limit"

    def _cc_exp_stop(self) -> str:
        """Stop the experiment scenario, if it is currently running."""
        ns = self._ns
        if not ns.scn_running:
            return "Network experiment scenario is not currently running"

        self._cb_scn_stop()

        return ""

    def _cc_list_commands(self) -> str:
        """List of valid commands."""
        return ', '.join(self._console_commands.keys())

    def _cc_list_env_keys(self) -> str:
        """List all environment keys."""
        env_key_names = self._env.env_key_names
        if not len(env_key_names):
            return "No available environment keys to list"

        val_lst = [["NAME"]]
        val_lst.extend([[env_key_full_name] for env_key_full_name in env_key_names])

        return self._format_list_output([''], val_lst)

    def _cc_list_envs(self) -> str:
        """List all loaded environments."""
        env_names = self._env.env_names
        if not len(env_names):
            return "No loaded environments to list"

        val_lst = [["NAME"]]
        val_lst.extend([[env_full_name] for env_full_name in env_names])

        return self._format_list_output([''], val_lst)

    def _cc_list_nodes(self) -> str:
        """List of running nodes."""
        val_lst = [["ID", "NAME", "TYPE", "ADDRESS", "CONN", "RTT (ms)", "RESP", "RCONN"]]
        for peer_node_id, node_data in self._ns.node_by_id.items():

            if node_data.is_connected:
                node_conn = "Y"
                node_rtt = f"{(node_data.rtt / 1000000.0):.3f}"  # milliseconds
                node_resp = "Y" if self._ns.is_responsive(peer_node_id) else "N"
            else:
                node_conn = "N"
                node_rtt = "-"
                node_resp = "N"

            val_lst.append([str(peer_node_id),
                            node_data.peer_node_name,
                            NAME_STR_NODE_TYPE[node_data.peer_node_type],
                            node_data.peer_address,
                            node_conn,
                            node_rtt,
                            node_resp,
                            str(node_data.connection_count - 1)])  # reconnects = connection_count - 1

        return self._format_list_output(['>', '', '', '', '', '>', '', '>'], val_lst)

    def _cc_list_services(self) -> str:
        """List all registered service instances."""
        service_instance_dct = self._ns.service_by_id
        if not len(service_instance_dct):
            return "No registered services to list"

        val_lst = [["ID", "NAME", "CONFIG", "CLASS", "NODE", "STATUS"]]
        for service_id, service_instance_data in service_instance_dct.items():

            if not service_instance_data.node_instance.is_connected and \
                    not service_instance_data.status == ServiceStatus.FAILED and \
                    not service_instance_data.status == ServiceStatus.EXIT:
                service_status = "UNKNOWN"
            else:
                service_status = service_instance_data.status.name

            val_lst.append([str(service_id),
                            service_instance_data.service_display_name,
                            service_instance_data.service_config.config_name,
                            service_instance_data.service_class.service_class_name,
                            str(service_instance_data.node_instance.peer_node_id),
                            service_status])

        return self._format_list_output(['>', '', '', '', '>', ''], val_lst)

    def _cc_uptime(self) -> str:
        """Duration hub node has been running since start() call."""
        return f"{time.ctime(time.time())}, hub running for {self.format_duration(time.monotonic() - self._start_time)}"

    def _cc_usage_process(self) -> str:
        """Resource usage of the hub."""
        with self._p_info.oneshot():
            cpu_percent = self._p_info.cpu_percent(interval=None)
            mem_percent = self._p_info.memory_percent(memtype='rss')
            mem_info = self._p_info.memory_info()
            mem_rss = mem_info.rss / 1048576.0
            mem_vms = mem_info.vms / 1048576.0

            mem_str = f"{mem_rss:.2f}M RSS, {mem_vms:.2f}M VMS"
            xtra_str = f"Open file descriptors: {self._p_info.num_fds()}"

        return f"Hub node process resource usage:\n" \
               f"- CPU: {cpu_percent:.1f}%\n- MEM: {mem_percent:.1f}%\n" \
               f"Memory: {mem_str}\n{xtra_str}"

    @staticmethod
    def _cc_usage_system() -> str:
        """Resource usage of the system hub is running on."""
        cpu_percent = psutil.cpu_percent(interval=None)
        mem_info = psutil.virtual_memory()
        mem_percent = mem_info.percent
        mem_total = mem_info.total / 1048576.0
        mem_avail = mem_info.available / 1048576.0

        mem_str = f"{mem_total:.2f}M total, {mem_avail:.2f}M available"
        xtra_str = f"System load: {psutil.getloadavg()} over {psutil.cpu_count()} CPUs"

        return f"System resource usage:\n"\
               f"- CPU: {cpu_percent:.1f}%\n- MEM: {mem_percent:.1f}%\n"\
               f"Memory: {mem_str}\n{xtra_str}"


class HubNode(NodeBase):
    """Hub node."""

    __slots__ = ('logger_dist', '_ns', '_cm', '_env', '_port', '_scn_timer', '_duration_hb', '_hb_timers')

    def __init__(self, system_config: Mapping):
        """Constructor."""
        super().__init__(system_config, NODE_TYPE_HUB)

        self.node_id = NODE_ID_HUB

        dist_logger = logging.getLogger("emews_hub_dist")
        dist_logger.setLevel(logging.DEBUG)
        dist_logger.propagate = False

        logger_dist_handler = HubLogNetHandler(self.node_name, self._monitors_send_log)
        logger_dist_handler.setLevel(system_config['logging']['log_message_level'])

        dist_logger.addHandler(logger_dist_handler)  # sending log messages to monitor nodes
        self.logger_dist = dist_logger

        self._port: int = system_config['communication']['port']

        self._scn_timer: Union[TimerEvent, None] = None

        if system_config['debug']['disable_heartbeat']:
            self.logger.warning("Node heartbeats disabled (as given in the system config)")
            duration_hb = -1
        else:
            duration_hb = system_config['hub']['heartbeat_duration']
            if duration_hb is None or duration_hb < 1:
                self.logger.warning("Heartbeat duration invalid, defaulting to 1 second")
                duration_hb = 1

        self._duration_hb = duration_hb
        self._hb_timers: Dict[TimerEvent, NodeData] = {}

        self._ns = NetState(system_config['hub']['scenario_autostart'],
                            system_config['hub']['scenario_autostart_delay'],
                            system_config['hub']['scenario_duration'])

        self._env = EnvManager(self.logger_dist, self._new_timer, self._event_close)

        self._ns.parse_services(self.logger)

        # pycharm - expected type warning due to pycharm not fully supporting Protocols
        self._cm = ConsoleManager(self.logger_dist, self._ns, self._env, self._send_net_request,
                                  self._start_scenario, self._stop_scenario)

        NET_PROTOCOL[NetProtocolID.HUB_LOGGING_MESSAGE].request_handler = self._handle_logging_message
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_REG].request_handler = self._handle_host_service_reg
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SEND_ALL].request_handler = self._handle_service_send_all
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SEND_TO].request_handler = self._handle_service_send_to
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_STARTED].request_handler = self._handle_service_started
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_STOPPED].request_handler = self._handle_service_stopped
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SPAWNED].request_handler = self._handle_service_spawned
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_EXITED].request_handler = self._handle_service_exited
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_TELL].request_handler = self._env.env_handle_new_obs
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_ASK].request_handler = self._env.env_handle_ev_request
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_ENVKEY_ID].request_handler = self._env.env_handle_envkey_id_req

        NET_PROTOCOL[NetProtocolID.HUB_HUBCONSOLE_WEL].request_handler = self._handle_hubconsole_welcome
        NET_PROTOCOL[NetProtocolID.HUB_CONSOLE_COMMAND].request_handler = self._cm.process_console_command

        NET_PROTOCOL[NetProtocolID.CLIENT_HEARTBEAT].response_handler = self._response_heartbeat
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_SPAWN].response_handler = self._response_ack_console_request
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_START].response_handler = self._response_ack_console_request
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_STOP].response_handler = self._response_ack_console_request

    def start(self) -> None:
        """Start the node."""
        self._env.parse_environments(self.logger)

        self._cm.start()

        if not self._add_listener(self._port, self._on_inbound_connected):
            return

        if self._ns.scn_autostart:
            self.logger.info("Experiment scenario autostart enabled")
            delay_scn_start = self._ns.scn_autostart_delay
            if delay_scn_start > 0:
                self._new_timer(delay_scn_start, self._handle_start_timer)
                self.logger.info("Waiting %d seconds to start experiment scenario ...", delay_scn_start)
            else:
                # start experiment scenario now
                self._start_scenario()

    def _new_timer(self, interval: int, on_timer_expiry: TimerEventCB, repeat=False) -> TimerEvent:
        """Wrapper for _add_timer(), includes set() call."""
        timer_event = self._add_timer(on_timer_expiry)
        timer_event.set(interval, repeat=repeat)
        return timer_event

    def _close_hb_timer(self, node_data: NodeData):
        """Close the heartbeat timer of a node."""
        hb_timer = node_data.hb_timer
        node_data.hb_timer = None
        del self._hb_timers[hb_timer]
        self._event_close(hb_timer)

    def _on_peer_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle a node disconnection."""
        node_data = self._ns.node_by_id[peer_node_id]

        self._close_hb_timer(node_data)

        if node_data.peer_node_type == NODE_TYPE_HOST and self._ns.scn_running:
            # host client nodes should not disconnect during an experiment run
            self.logger_dist.warning(log_msg)
        else:
            self.logger_dist.info(log_msg)

    def _on_inbound_connected(self, inbound_conn_event: InboundEvent,
                              received_node_name: str, received_node_type: int, received_num_conn: int) -> None:
        """Handle inbound connection establishment."""
        peer_address = inbound_conn_event.peer_addr

        if received_node_name == self.node_name:
            self.logger_dist.warning("Node at %s has the same node name - '%s' - as the hub (node type: %d)",
                                     peer_address, received_node_name, received_node_type)
            self._event_close(inbound_conn_event)
            return

        if received_node_type == NODE_TYPE_HOSTPROC:
            # only client node types are serviceable (nodes that inherent from ClientNode)
            self.logger_dist.warning("Node '%s' at %s is not of a node type serviceable by the hub (node type: %d)",
                                     received_node_name, peer_address, received_node_type)
            self._event_close(inbound_conn_event)
            return

        node_data = self._ns.node_by_name.get(received_node_name)

        if node_data is None:
            # new node (first time connection)
            node_data = self._ns.new_node_instance(received_node_name, received_node_type, peer_address)
            peer_node_id = node_data.peer_node_id

            self._add_connection(inbound_conn_event, node_data, self._on_peer_disconnection,
                                 event_class=HubConnectionEvent)
            node_data.write_data(struct.pack('>LH', peer_node_id, NODE_TYPE_HUB))

            self.logger_dist.info("Node '%s' at %s connected (assigned node id: %d, node type: %d)",
                                  received_node_name, peer_address, peer_node_id, received_node_type)

            if received_node_type == NODE_TYPE_HOST and self._ns.scn_running:
                # this host node is late to the party
                self._send_net_request(node_data, NetProtocolID.CLIENT_SCENARIO_START)
        else:
            # reconnection
            peer_node_id = node_data.peer_node_id

            if received_node_type != node_data.peer_node_type:
                self.logger_dist.warning("Incoming connection with node %d at %s: received node type mismatch "
                                         "(node name: %s, node type: %d, received node type: %d)", peer_node_id,
                                         peer_address, received_node_name, node_data.peer_node_type, received_node_type)
                self._event_close(inbound_conn_event)
                return

            if received_node_type == NODE_TYPE_HOST and received_num_conn != node_data.connection_count:
                self.logger_dist.warning("Incoming connection with node %d at %s: received host node reconnection "
                                         "count mismatch, host gave %d, but was expecting %d (node name: %s)",
                                         peer_node_id, peer_address,
                                         received_num_conn, node_data.connection_count, received_node_name)
                self._event_close(inbound_conn_event)
                return

            if node_data.is_connected:
                # This node's previous connection is still open.
                # Prior behavior was to kill the existing connection (in case the existing connection was a zombie),
                # but that opens the possibility of 'oscillating' connections between competing nodes of the same name,
                # where each node kicks the other off.  Now existing connections are assumed valid until they close,
                # or until they have been unresponsive for a set period of time.
                if self._ns.is_responsive(peer_node_id):
                    self.logger_dist.debug("Incoming connection with node %d at %s: another connection with this node "
                                           "is still active (node name: %s, node type: %d)", peer_node_id, peer_address,
                                           received_node_name, received_node_type)
                    self._event_close(inbound_conn_event)
                    return

                self.logger_dist.info("Incoming connection with node %d at %s: another connection with this node is "
                                      "still active (node name: %s, node type: %d) but is unresponsive, closing it ...",
                                      peer_node_id, peer_address, received_node_name, received_node_type)
                self._event_close(node_data.conn_event)
                self._close_hb_timer(node_data)

            self._add_connection(inbound_conn_event, node_data, self._on_peer_disconnection,
                                 event_class=HubConnectionEvent)
            node_data.write_data(struct.pack('>LH', peer_node_id, NODE_TYPE_HUB))

            if peer_address != node_data.peer_address:
                self.logger_dist.info("Node %d at %s (formerly at %s) reconnected (node name: %s, node type: %d, "
                                      "connection count: %d)", peer_node_id, peer_address, node_data.peer_address,
                                      received_node_name, received_node_type, node_data.connection_count)

                node_data.peer_address = peer_address
            else:
                self.logger_dist.info("Node %d at %s reconnected (node name: %s, node type: %d, connection count: %d)",
                                      peer_node_id, peer_address, received_node_name, received_node_type,
                                      node_data.connection_count)

            # reconnections may have pending requests
            for pending_request in node_data.pending_requests:
                node_data.write_data(pending_request[0])

        # start RTT
        hb_timer = self._new_timer(self._duration_hb, self._handle_heartbeat_ex, repeat=True)
        node_data.hb_timer = hb_timer
        self._hb_timers[hb_timer] = node_data

    def _start_scenario(self) -> None:
        """Run a network experiment scenario."""
        ndr = self._ns

        duration_scn = ndr.scn_duration
        if duration_scn > 0:
            self._scn_timer = self._new_timer(duration_scn, self._handle_scn_duration_timer)
            self.logger_dist.info("Network experiment scenario starting, will run for a duration of %d seconds",
                                  duration_scn)
        else:
            # if 0, unlimited duration
            self.logger_dist.info("Network experiment scenario starting, will run without duration limit")

        if len(ndr.active_nodes):
            self.logger_dist.info("Notifying client nodes that experiment scenario is starting ...")
            for node_data in ndr.active_nodes:
                self._send_net_request(node_data, NetProtocolID.CLIENT_SCENARIO_START)

        ndr.scn_start()

    def _stop_scenario(self) -> None:
        """Stop a running network experiment scenario."""
        self._ns.scn_stop()

        if self._scn_timer is not None:
            self._event_close(self._scn_timer)
            self._scn_timer = None

        self.logger_dist.info("Network experiment scenario finished")

        self.logger_dist.info("Notifying host nodes that experiment scenario has finished ...")
        for node_data in self._ns.active_hosts:
            self._send_net_request(node_data, NetProtocolID.CLIENT_SCENARIO_STOP)

    def _monitors_send_log(self, node_name: bytes, node_id: int, levelno: int, msg: bytes) -> None:
        """Send the log message to all monitors."""

        if levelno == logging.WARNING:
            self._ns.log_warnings += 1
        elif levelno == logging.ERROR:
            self._ns.log_errors += 1

        for node_data in self._ns.active_monitors:
            self._send_net_request_nr(node_data, NetProtocolID.HUBMON_LOGGING_MESSAGE,
                                      request_data=(node_id, node_name, msg))

    # request/response methods
    # noinspection PyUnusedLocal
    def _handle_start_timer(self, timer_event, num_expires):
        """Start the experiment scenario (from timer delay)."""
        self._event_close(timer_event)
        self._start_scenario()

    # noinspection PyUnusedLocal
    def _handle_heartbeat_ex(self, timer_event, num_expires):
        """Send a heartbeat to client corresponding to timer."""
        if num_expires > 1:
            warn_msg = "Heartbeat timer expired multiple times before handler invocation (expiry count: " \
                       f"{num_expires}, heartbeat interval: {self._duration_hb}), hub node may be overloaded ..."
            self.logger.warning(warn_msg)
            self.logger_dist.warning(warn_msg)

        node_data = self._hb_timers[timer_event]

        if node_data.hb_missed:
            # Have not received ACK from last heartbeat.  Do not send another heartbeat.
            if node_data.is_responsive:
                self.logger_dist.warning("Node %d is no longer responsive", node_data.peer_node_id)
                node_data.is_responsive = False
        else:
            self._send_net_request(node_data, NetProtocolID.CLIENT_HEARTBEAT, local_data=time.perf_counter_ns())
            node_data.hb_missed = True

    # noinspection PyUnusedLocal
    def _handle_scn_duration_timer(self, timer_event, num_expires):
        """Stop experiment scenario."""
        assert timer_event == self._scn_timer

        self._event_close(timer_event)
        self._scn_timer = None
        self._stop_scenario()

    ############################
    # network request handlers #
    ############################
    def _handle_logging_message(self, node_id: int, levelno: int, msg: bytes) -> tuple:
        """Forward log message from peer to monitors."""
        self._monitors_send_log(bytes(self._ns.node_by_id[node_id].peer_node_name, STR_ENCODING), node_id, levelno, msg)
        return ()

    def _handle_hubconsole_welcome(self, node_id: int) -> tuple:
        """Send welcome message to console."""
        assert self._ns.node_by_id[node_id].peer_node_type == NODE_TYPE_HUBCONSOLE

        welcome_msg = self._cm.welcome_msg(self.node_name)
        return bytes(self.node_name, STR_ENCODING), bytes(welcome_msg, STR_ENCODING)

    def _handle_host_service_reg(self, node_id: int, service_name: bytes, config_filename: bytes) -> tuple:
        """Registers a new service for a host node"""
        node_data = self._ns.node_by_id[node_id]

        service_instance_data = self._ns.new_service_instance(
            service_name.decode(), config_filename.decode(), node_data)

        service_id = service_instance_data.service_id

        self.logger_dist.info("Node %d registered instance of service '%s', assigned service id %d",
                              node_id, service_instance_data.full_name, service_id)

        return service_id, bytes(service_instance_data.service_display_name, STR_ENCODING)

    def _handle_service_send_all(self, node_id: int, from_service_id: int, data: bytes) -> tuple:
        """Send data to all running services based on send/recv service class matching."""
        ns = self._ns

        try:
            service_instance_data = ns.service_by_id[from_service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{from_service_id}' does not exist (request from node {node_id})")

        if service_instance_data.node_instance.peer_node_id != node_id:
            raise NetworkHandlerError(f"service id '{from_service_id}' is assigned to node "
                                      f"{service_instance_data.node_instance.peer_node_id}, not node {node_id}")

        self.logger_dist.info("Sending message to all from service %d (service name: %s)",
                              from_service_id, service_instance_data.full_name)

        send_to_classes = service_instance_data.service_config.send_to

        # this gives us all service instances who list this service instance as being able to recv data from
        for recv_instance in ns.active_receivers[service_instance_data.service_class]:
            # need to check if this receive instance belongs to a class we can send to
            if recv_instance.service_class not in send_to_classes:
                continue

            node_data = recv_instance.node_instance
            to_service_id = recv_instance.service_id
            self.logger.debug(
                "Sending message from service %d (service name: %s) to service %d (service name: %s, node id: %d)",
                from_service_id, service_instance_data.full_name, to_service_id, recv_instance.full_name,
                node_data.peer_node_id)
            self._send_net_request(node_data, NetProtocolID.HOST_SERVICE_SEND_MSG,
                                   request_data=(from_service_id, to_service_id, data))

        return ()

    def _handle_service_send_to(self, node_id: int, from_service_id: int, to_services: bytes, data: bytes) -> tuple:
        """Send data to all running services in to_services list based on send/recv service class matching."""
        ns = self._ns

        try:
            service_instance_data = ns.service_by_id[from_service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{from_service_id}' does not exist (request from node {node_id})")

        if service_instance_data.node_instance.peer_node_id != node_id:
            raise NetworkHandlerError(f"service id '{from_service_id}' is assigned to node "
                                      f"{service_instance_data.node_instance.peer_node_id}, not node {node_id}")

        self.logger_dist.info("Sending message to recipients from service %d (service name: %s)",
                              from_service_id, service_instance_data.full_name)

        service_id_lst: Tuple[int] = pickle.loads(to_services)
        send_to_classes = service_instance_data.service_config.send_to
        service_class_data = service_instance_data.service_class

        for to_service_id in service_id_lst:
            to_service_instance = ns.service_by_id[to_service_id]
            to_service_class = to_service_instance.service_class
            # need to check if this to_service instance's class is in our send to set, and if the service_instance_data
            # class is in the to_service's receive from set
            if to_service_class not in send_to_classes:
                self.logger_dist.warning(
                    "Could not send message from service %d to service %d: class '%s' not specified for sending to",
                    from_service_id, to_service_id, to_service_class.service_class_name)
                continue
            if to_service_class not in ns.active_receivers[service_class_data]:
                self.logger_dist.warning(
                    "Could not send message from service %d to service %d: class '%s' not specified for receiving from",
                    from_service_id, to_service_id, service_class_data.service_class_name)
                continue

            node_data = to_service_instance.node_instance
            self.logger.debug(
                "Sending message from service %d (service name: %s) to service %d (service name: %s, node id: %d)",
                from_service_id, service_instance_data.full_name, to_service_id, to_service_instance.full_name,
                node_data.peer_node_id)
            self._send_net_request(node_data, NetProtocolID.HOST_SERVICE_SEND_MSG,
                                   request_data=(from_service_id, to_service_id, data))

        return ()

    def _handle_service_started(self, node_id: int, service_id: int) -> tuple:
        """A service instance has started on the host."""
        try:
            service_instance_data = self._ns.service_by_id[service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{service_id}' does not exist (request from node {node_id})")

        if service_instance_data.status != ServiceStatus.READY:
            raise NetworkHandlerError(f"node {node_id} started service {service_id} that was not ready")

        service_instance_data.status = ServiceStatus.RUNNING
        return ()

    def _handle_service_stopped(self, node_id: int, service_id: int) -> tuple:
        """A service instance has stopped on the host."""
        try:
            service_instance_data = self._ns.service_by_id[service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{service_id}' does not exist (request from node {node_id})")

        if service_instance_data.status != ServiceStatus.RUNNING:
            raise NetworkHandlerError(f"node {node_id} stopped service {service_id} that was not running")

        service_instance_data.status = ServiceStatus.READY
        return ()

    def _handle_service_spawned(self, node_id: int, service_id: int, is_instantiated: bool) -> tuple:
        """
        A service has fully spawned on the host.

        The instantiation state of the service is expected not to change throughout the duration of the host, as
        services are only instantiated once, when they are spawned."""
        ns = self._ns

        try:
            service_instance_data = ns.service_by_id[service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{service_id}' does not exist (request from node {node_id})")

        # if service instantiated, then the service thread is ready to start, else the service failed
        if is_instantiated:
            for recv_class in service_instance_data.service_config.receive_from:
                ns.active_receivers[recv_class].add(service_instance_data)

            service_instance_data.status = ServiceStatus.READY
        else:
            service_instance_data.status = ServiceStatus.FAILED

        return ()

    def _handle_service_exited(self, node_id: int, service_id: int, is_failed: bool) -> tuple:
        """A service has shutdown (service thread stopped) on the host."""
        ns = self._ns
        try:
            service_instance_data = ns.service_by_id[service_id]
        except KeyError:
            raise NetworkHandlerError(f"service id '{service_id}' does not exist (request from node {node_id})")

        for recv_class in service_instance_data.service_config.receive_from:
            ns.active_receivers[recv_class].remove(service_instance_data)

        if is_failed:
            # service exited because it threw an exception
            service_instance_data.status = ServiceStatus.FAILED
        else:
            service_instance_data.status = ServiceStatus.EXIT

        return ()

    # response handlers
    def _response_heartbeat(self, node_id: int, last_ts: int):
        """Calculate RTT"""
        current_ts = time.perf_counter_ns()
        node_data = self._ns.node_by_id[node_id]

        if not node_data.is_responsive:
            # this node was lagging but recovered
            self.logger_dist.info("Node %d is responsive again", node_data.peer_node_id)
            node_data.is_responsive = True

        node_data.hb_missed = False
        node_data.rtt = current_ts - last_ts  # nanoseconds

    def _response_ack_console_request(self, node_id: int, req_str: str):
        """Ack from a console-originated request."""
        self.logger_dist.debug("Node %d acknowledged console-originated request: %s", node_id, req_str)
