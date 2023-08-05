"""Host process nodes module.  These nodes connect locally to the running host node."""
from typing import Mapping

from emews.base.node import STR_ENCODING, NODE_ID_UNASSIGNED, NODE_TYPE_HOST, NODE_TYPE_HOSTPROC, ConnectionState,\
    LocalConnectionEvent, NetProtocolID, NET_PROTOCOL, NodeBase, OutboundEvent, PeerResponseError


class HostProc(NodeBase):
    """Host node process.  Connects to local host node."""

    __slots__ = ('_port', '_reconnect_delay', '_host_conn')

    def __init__(self, system_config: Mapping):
        """Constructor."""
        super().__init__(system_config, NODE_TYPE_HOSTPROC)

        comm_config = system_config['communication']
        debug_host_port = system_config['debug']['host_port']

        if debug_host_port is not None:
            self._port = debug_host_port
        else:
            self._port = comm_config['port']

        self._reconnect_delay = comm_config['reconnect_delay']

        # HostProc doesn't process any incoming requests
        self._host_conn = ConnectionState(NODE_ID_UNASSIGNED, NODE_TYPE_HOST, comm_config['local_address'])

    def start(self) -> None:
        """Start the local process."""
        self._connect_host()

    def _on_peer_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle a node disconnection."""
        self.logger.warning(log_msg)
        self._reconnect_timer()

    def _on_host_connect_failed(self, host_address: str, reason: str) -> None:
        """Connection attempt to the host failed."""
        assert host_address == self._host_conn.peer_address

        self.logger.warning("Connection attempt to the local host node at %s failed: %s", host_address, reason)
        self._reconnect_timer()

    def _on_outbound_connected(self, outbound_conn_event: OutboundEvent,
                               received_node_id: int, received_node_type: int) -> None:
        """Connection attempt to the hub succeeded."""
        host_address = self._host_conn.peer_address
        assert outbound_conn_event.peer_addr == host_address

        if received_node_type != NODE_TYPE_HOST:
            raise PeerResponseError(f"Local connection at {host_address}: expected host node type {NODE_TYPE_HOST}, "
                                    f"but received node type {received_node_type}.  Is this the local host node?")

        self._add_connection(outbound_conn_event, self._host_conn, self._on_peer_disconnection,
                             event_class=LocalConnectionEvent)

        self.logger.info("Connected to the local host node at %s (connection count: %d)",
                         host_address, self._host_conn.connection_count)

        for pending_request in self._host_conn.pending_requests:
            self._host_conn.write_data(pending_request[0])

    def _connect_host(self) -> None:
        """Initiate an outbound connection attempt to the host node."""
        self._add_outbound_connecting(self._port, self._host_conn,
                                      self._on_host_connect_failed, self._on_outbound_connected)

        self.logger.info("Connecting to the local host node at %s, port %d ...",
                         self._host_conn.peer_address, self._port)

    def _reconnect_timer(self):
        """Create a new timer to act as a delay for peer reconnection attempt."""
        timer_event = self._add_timer(self._handle_reconnect_timer)
        timer_event.set(self._reconnect_delay)
        self.logger.info("Waiting %d seconds before reconnecting ...", self._reconnect_delay)

    def _handle_reconnect_timer(self, timer_event, num_expires):
        """Handle reconnect timer expiration."""
        self._event_close(timer_event)
        # the timer should only expire once, multiple expires suggests polling loop is lagging
        self.logger.debug("Host reconnection timer expiry count: %d", num_expires)
        self._connect_host()


class ServiceSpawner(HostProc):
    """Request host to spawn service."""
    __slots__ = ('_service_name', '_service_config_filename')

    def __init__(self, system_config: Mapping, service_name: str, service_config_filename: str):
        """Constructor."""
        super().__init__(system_config)

        NET_PROTOCOL[NetProtocolID.HOST_SERVICE_LOCAL_REQ].response_handler = self._response_service_req

        self._service_name = service_name
        self._service_config_filename = service_config_filename

    def start(self) -> None:
        """Start the local process."""
        self.logger.info("Service to spawn: %s, configuration: %s",
                         self._service_name, self._service_config_filename)
        super().start()
        self._send_net_request(self._host_conn, NetProtocolID.HOST_SERVICE_LOCAL_REQ,
                               (bytes(self._service_name, STR_ENCODING),
                                bytes(self._service_config_filename, STR_ENCODING)))

    def _response_service_req(self, peer_node_id: int, local_data):
        """Ack from host to acknowledge service request."""
        self.logger.info("Service spawn request acknowledged, shutting down process...")
        self.stop()
