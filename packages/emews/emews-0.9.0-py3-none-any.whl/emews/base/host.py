"""Host client node module."""
from typing import Dict, Mapping, Set, Tuple, Type

import struct
import threading

from emews.base.client import SynchronizedClientNode
from emews.base.env_key import EnvironmentKey
from emews.base.node import NET_PROTOCOL, NetProtocolID, NODE_ID_HUB, NODE_ID_UNASSIGNED, NODE_TYPE_HOST,\
    NODE_TYPE_HOSTPROC, TYPE_LEN, STR_ENCODING, NetworkHandlerError, InboundEvent, ConnectionState, LocalConnectionEvent
from emews.base.service import load_service, ServiceControlError, ServiceLoadError, Service, ServiceImpl

TYPE_LEN_INT = TYPE_LEN['L']


class HostNode(SynchronizedClientNode):
    """Host client node.  These nodes run services."""

    __slots__ = ('_port', '_services', '_timeout_service_shutdown', '_env_keys', '_env_key_pending', '_env_key_cv',
                 '_is_scn_started')

    def __init__(self, system_config: Mapping):
        """Constructor."""
        super().__init__(system_config, NODE_TYPE_HOST)

        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_SEND_MSG].request_handler = self._handle_service_recv_msg
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_SPAWN].request_handler = self._handle_cmd_service_spawn
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_START].request_handler = self._handle_cmd_service_start
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_STOP].request_handler = self._handle_cmd_service_stop
        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_LOCAL_REQ].request_handler = self._handle_local_service_spawn

        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_REG].response_handler = self._response_hub_service_reg
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SEND_ALL].response_handler = self._response_unblock_service
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SEND_TO].response_handler = self._response_unblock_service
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_TELL].response_handler = self._response_unblock_service
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_ASK].response_handler = self._response_env_ask
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_ENVKEY_ID].response_handler = self._response_env_key_id
        NET_PROTOCOL[NetProtocolID.HUB_SERVICE_SPAWNED].response_handler = self._response_hub_service_spawned

        debug_config = system_config['debug']
        debug_host_port = debug_config['host_port']

        if debug_host_port is not None:
            self._port = debug_host_port
        else:
            self._port = self._hub_port

        self._services: Dict[int, ServiceImpl] = {}  # all services (key=service id)

        self._env_keys: Dict[EnvironmentKey, int] = {}  # cached key enum -> key id
        self._env_key_pending: Set[EnvironmentKey] = set()  # key id requests not received yet
        self._env_key_cv = threading.Condition()  # sync access to env_key dict

        self._is_scn_started = False

        timeout_service_shutdown = system_config['general']['service_shutdown_timeout']
        if timeout_service_shutdown is None or timeout_service_shutdown < 1:
            self._timeout_service_shutdown = 1
        else:
            self._timeout_service_shutdown = timeout_service_shutdown

    def start(self) -> None:
        """Start the node."""
        if self._add_listener(self._port, self._on_inbound_connected):
            super().start()

    def shutdown(self) -> None:
        """Shutdown all services."""
        self.logger.info("Will wait up to %d seconds for each service to stop", self._timeout_service_shutdown)

        active_services = []
        for service in self._services.values():
            if service.is_active():
                try:
                    service.exit()
                except ServiceControlError as ex:
                    err_msg = f"On attempted service exit: {ex}"
                    self.logger.warning(err_msg)
                    self.logger_dist.warning(err_msg)
                else:
                    service.service_thread.join(self._timeout_service_shutdown)
                    if service.is_active():
                        # service is still running, join timeout reached
                        active_services.append(service.name)

        if len(active_services):
            self.logger.warning("%d services are still running: [%s], continuing shutdown",
                                len(active_services), ", ".join(active_services))
        else:
            self.logger.info("All running services shutdown")

    def _on_local_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle a local disconnection."""
        assert peer_node_id == NODE_ID_UNASSIGNED
        self.logger.debug(log_msg)

    def _on_inbound_connected(self, inbound_conn_event: InboundEvent,
                              received_node_name: str, received_node_type: int, received_num_conn: int) -> None:
        """Handle incoming local connection for local requests."""
        peer_addr = inbound_conn_event.peer_addr
        if not peer_addr.startswith('127.0.'):
            self.logger.warning("Incoming connection is non-local (address: %s, received node name: %s, "
                                "received node type: %d), dropping ...",
                                peer_addr, received_node_name, received_node_type)
            self._event_close(inbound_conn_event)
            return

        if received_node_type != NODE_TYPE_HOSTPROC:
            self.logger.warning("Incoming connection at %s: Expected node type %d, instead received node type %d",
                                peer_addr, NODE_TYPE_HOSTPROC, received_node_type)
            self._event_close(inbound_conn_event)
            return

        local_conn_state = ConnectionState(NODE_ID_UNASSIGNED, received_node_type, peer_addr)
        self._add_connection(inbound_conn_event, local_conn_state, self._on_local_disconnection,
                             event_class=LocalConnectionEvent)

        self.logger.info("Local connection at %s: host process '%s' connected", peer_addr, received_node_name)

        # send our node id and type
        # TODO: If HostProc needs our node id, wait to send until we have our node id from hub
        local_conn_state.write_data(struct.pack('>LH', self.node_id, self.node_type))

    def _service_start(self, service: ServiceImpl) -> None:
        """Start the service given."""
        service_name = service.name

        info_msg = f"Starting service '{service_name}' ..."
        self.logger.info(info_msg)
        self.logger_dist.info(info_msg)

        try:
            service.start()
        except ServiceControlError as ex:
            err_msg = f"On start for service '{service_name}': {ex}"
            self.logger.warning(err_msg)
            self.logger_dist.warning(err_msg)

    def _service_stop(self, service: ServiceImpl) -> None:
        """Stop the service given."""
        service_name = service.name

        info_msg = f"Stopping service '{service_name}' ..."
        self.logger.info(info_msg)
        self.logger_dist.info(info_msg)

        try:
            service.stop()
        except ServiceControlError as ex:
            err_msg = f"On stop for service '{service_name}': {ex}"
            self.logger.warning(err_msg)
            self.logger_dist.warning(err_msg)

    def _on_scenario_start(self) -> None:
        """Start all services."""
        self._is_scn_started = True
        self.logger.info("Experiment scenario has started, starting %d services ...", len(self._services))
        self.logger_dist.info("Starting %d services ...", len(self._services))

        for service in self._services.values():
            self._service_start(service)

    def _on_scenario_end(self) -> None:
        """Stop all services."""
        self._is_scn_started = False

        running_services = []

        for service in self._services.values():
            if service.is_running():
                running_services.append(service)

        self.logger.info("Experiment scenario has ended, stopping %d running services ...", len(self._services))
        self.logger_dist.info("Stopping %d running services ...", len(running_services))

        for service in running_services:
            self._service_stop(service)

    ##################################################
    # synchronized methods (these run from any thread)
    ##################################################
    def _sync_get_env_key_id(self, env_key: EnvironmentKey) -> int:
        """
        Fetch the key id given key enum.

        This method will always return the key id, blocking if the id needs to be fetched.
        """
        with self._env_key_cv:
            try:
                env_key_id = self._env_keys[env_key]
            except KeyError:
                if env_key not in self._env_key_pending:
                    # we need to request the key id from the hub
                    self._env_key_pending.add(env_key)
                    self._send_hub_request(NetProtocolID.HUB_SERVICE_ENVKEY_ID,
                                           request_data=(bytes(env_key.key_full_name(), STR_ENCODING),),
                                           local_data=env_key)

                    self.logger.debug("Requesting key id for environment key '%s' (%s)",
                                      env_key.key_full_name(), str(env_key))

                # block the service thread until the key id is fetched, then return it
                while env_key in self._env_key_pending:
                    # Releases lock on wait, acquires it when done waiting.  Note that if multiple
                    # keys are being requested, this service may awaken from another fulfilled
                    # request, in which case 'env_key' will still be in the pending set, and this
                    # service will continue to wait.
                    self._env_key_cv.wait()

                env_key_id = self._env_keys[env_key]

            return env_key_id

    def _sync_service_init(self, service: ServiceImpl, ex: Exception = None, exc_trace: str = None) -> None:
        """Service instantiation result."""
        self._sync_add_task(self._task_service_init, service, ex, exc_trace)

    def _sync_service_exit(self, service: ServiceImpl, ex: Exception = None, exc_trace: str = None) -> None:
        """Service exit result."""
        self._sync_add_task(self._task_service_exit, service, ex, exc_trace)

    #############################################
    # thread tasks (these run in the main thread)
    #############################################
    def _task_service_init(self, service: ServiceImpl, ex: Exception = None, exc_trace: str = None) -> None:
        """Service has finished instantiating (or failed to instantiate)."""
        if ex is not None:
            self.logger.error("Service '%s' did not instantiate: %s\n%s", service.name, ex, exc_trace)
        else:
            self.logger.info("Service '%s' instantiated", service.name)

        self._send_hub_request(NetProtocolID.HUB_SERVICE_SPAWNED, request_data=(service.service_id, ex is None),
                               local_data=service)

    def _task_service_exit(self, service: ServiceImpl, ex: Exception = None, exc_trace: str = None) -> None:
        """Service thread has terminated."""
        if ex is not None:
            self.logger.error("Service '%s' terminated unexpectedly: %s\n%s", service.name, ex, exc_trace)
        else:
            self.logger.info("Service '%s' shutdown successful", service.name)

        self._send_hub_request(NetProtocolID.HUB_SERVICE_EXITED, request_data=(service.service_id, ex is not None))

    ##########################
    # network request handlers
    ##########################
    def _handle_service_recv_msg(self, node_id: int, from_service_id: int, to_service_id: int, data: bytes) -> tuple:
        """Delegate received data to service instance with service id."""
        assert node_id == NODE_ID_HUB

        try:
            service = self._services[to_service_id]
        except KeyError:
            # indicates a bug in the hub
            self.logger_dist.error("Service with id %d is not registered to us", to_service_id)
            return ()

        service.recv_data(from_service_id, data)

        return ()

    def _handle_cmd_service_start(self, node_id: int, service_id: int) -> tuple:
        """Start a service registered to us."""
        assert node_id == NODE_ID_HUB

        try:
            service = self._services[service_id]
        except KeyError:
            # indicates a bug in the hub
            self.logger_dist.error("Service with id %d is not registered to us", service_id)
        else:
            self._service_start(service)

        return ()

    def _handle_cmd_service_stop(self, node_id: int, service_id: int) -> tuple:
        """Stop a service registered to us."""
        assert node_id == NODE_ID_HUB

        try:
            service = self._services[service_id]
        except KeyError:
            # indicates a bug in the hub
            self.logger_dist.warning("Service with id %d is not registered to us", service_id)
        else:
            self._service_stop(service)

        return ()

    def _handle_cmd_service_spawn(self, node_id: int, service_name: bytes, config_filename: bytes,
                                  service_id: int, service_display_name: bytes) -> tuple:
        """Spawn a service, requested by the hub (probably from a console)."""
        assert node_id == NODE_ID_HUB

        service_name_str = service_name.decode()
        config_filename_str = config_filename.decode()

        try:
            service_class, service_config = load_service(service_name_str, config_filename_str)
        except ServiceLoadError as ex:
            raise NetworkHandlerError(ex) from ex

        self.logger.info("New service spawn remote request for service '%s' with configuration '%s'",
                         service_name_str, config_filename_str)

        # instantiate using the response method for service reg
        self._response_hub_service_reg(node_id,
                                       (service_class, service_name_str, service_config, config_filename_str),
                                       service_id, service_display_name)

        return ()

    def _handle_local_service_spawn(self, node_id: int, service_name: bytes, config_filename: bytes) -> tuple:
        """Import a service.  Request service information from hub."""
        assert node_id == NODE_ID_UNASSIGNED  # from local service request process

        service_name_str = service_name.decode()
        config_filename_str = config_filename.decode()

        try:
            service_class, service_config = load_service(service_name_str, config_filename_str)
        except ServiceLoadError as ex:
            raise NetworkHandlerError(ex) from ex

        self.logger.info("New service spawn request for service '%s' with configuration '%s'",
                         service_name_str, config_filename_str)

        self._send_hub_request(NetProtocolID.HUB_SERVICE_REG,
                               request_data=(service_name, config_filename),
                               local_data=(service_class, service_name_str, service_config, config_filename_str))

        return ()

    ###########################
    # network response handlers
    ###########################
    def _response_hub_service_reg(self, node_id: int, local_data: Tuple[Type[Service], str, Dict, str],
                                  service_id: int, service_display_name: bytes) -> None:
        """Complete service initialization (spawn)."""
        assert node_id == NODE_ID_HUB
        service_class, service_name, service_config, config_filename = local_data

        service_logger = self._get_dist_logger(f"emews_service.{service_id}")
        service_full_name = f"[{service_id}]{service_display_name.decode()}.{config_filename}"

        info_msg = f"Instantiating service '{service_name}' (assigned id: {service_id}) as '{service_full_name}' ..."
        self.logger.info(info_msg)
        self.logger_dist.info(info_msg)

        service = ServiceImpl(self.logger_dist, service_id, service_full_name,
                              (service_logger, service_class, service_config,
                               self._sync_service_init, self._sync_service_exit),
                              self._sync_get_env_key_id,
                              self._send_hub_request)

        self._services[service_id] = service

        service.service_thread.start()

    def _response_hub_service_spawned(self, node_id: int, service: ServiceImpl) -> None:
        """ACK from hub node of service spawned / instantiation result."""
        assert node_id == NODE_ID_HUB

        if self._is_scn_started:
            self._service_start(service)

    @staticmethod
    def _response_unblock_service(node_id: int, service_event: threading.Event):
        """Hub response from a blocking service request."""
        assert node_id == NODE_ID_HUB

        service_event.set()  # unblock service that sent request

    @staticmethod
    def _response_env_ask(node_id: int, local_data: Tuple[threading.Event, EnvironmentKey, list], env_data: bytes):
        """Env data from a service ask request."""
        assert node_id == NODE_ID_HUB

        service_event, ev_key, ev_lst = local_data

        assert not len(ev_lst)

        num_ev_val: int = struct.unpack_from(">L", env_data)[0]
        ev_lst.extend(struct.unpack_from(f">{ev_key.key_list_type * num_ev_val}", env_data, offset=TYPE_LEN_INT))
        service_event.set()  # unblock service (service has reference to ev_lst)

    def _response_env_key_id(self, node_id: int, env_key: EnvironmentKey, env_key_id: int):
        """Environment key id from a env key request."""
        assert node_id == NODE_ID_HUB

        with self._env_key_cv:
            self._env_keys[env_key] = env_key_id
            self._env_key_pending.remove(env_key)

            # This will wake up any services waiting for any key request.  Those not waiting on this
            # specific key will continue to wait after checking the key pending set.
            self._env_key_cv.notify_all()

        self.logger.debug("Environment key '%s' has assigned key id %d", env_key.key_full_name(), env_key_id)
