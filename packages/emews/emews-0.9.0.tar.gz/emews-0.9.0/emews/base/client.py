"""Client nodes module."""
from typing import Any, Callable, List, Mapping, Sequence, Tuple

import logging
import threading

from emews.base.node import NET_PROTOCOL, NODE_ID_HUB, NODE_ID_UNASSIGNED, NODE_TYPE_HUB, ConnectionState,\
    log_record_make_pickle, NodeBase, OutboundEvent, NetProtocolID, PeerResponseError, CounterEvent


class LogNetHandler(logging.Handler):
    """Logging handler for distributed logging."""

    def __init__(self, log_send_cb: Callable[[int, Sequence], None]):
        """Constructor."""
        super().__init__()
        self._log_send_cb = log_send_cb  # send log callback

    def emit(self, record):
        """Emit a log record."""
        pickled_log = log_record_make_pickle(record, self.format)
        self._log_send_cb(NetProtocolID.HUB_LOGGING_MESSAGE, (record.levelno, pickled_log,))


class ClientNode(NodeBase):
    """Client node base.  These nodes makes connections to the hub."""

    __slots__ = ('logger_dist', '_dist_log_level', '_hub_port', '_hub_reconnect_delay', '_hub_conn')

    def __init__(self, system_config: Mapping, node_type: int):
        """Constructor."""
        super().__init__(system_config, node_type)

        NET_PROTOCOL[NetProtocolID.CLIENT_HEARTBEAT].request_handler = self._handle_heartbeat
        NET_PROTOCOL[NetProtocolID.CLIENT_SCENARIO_START].request_handler = self._handle_scenario_start
        NET_PROTOCOL[NetProtocolID.CLIENT_SCENARIO_STOP].request_handler = self._handle_scenario_stop

        self._dist_log_level = system_config['logging']['log_message_level']

        self.logger_dist = self._get_dist_logger("emews_client_dist")

        comm_config = system_config['communication']
        self._hub_port: int = comm_config['port']
        self._hub_reconnect_delay = comm_config['reconnect_delay']

        self._hub_conn = ConnectionState(NODE_ID_HUB, NODE_TYPE_HUB, system_config['hub']['address'])

        start_delay = system_config['general']['node_start_delay']
        if start_delay > 0:
            self.logger.info("Waiting %d seconds before proceeding ...", start_delay)
            threading.Event().wait(start_delay)

    def _get_dist_logger(self, name: str) -> logging.Logger:
        """Returns a distributed logger based on name, and a new instance if name is unique."""
        dist_logger = logging.getLogger(name)

        if dist_logger.hasHandlers():
            # looks like the name was used previously
            return dist_logger

        dist_logger.setLevel(logging.DEBUG)
        dist_logger.propagate = False  # don't propagate messages up to (logging) root

        dist_logger_handler = LogNetHandler(self._send_hub_request_nr)
        dist_logger_handler.setLevel(self._dist_log_level)

        dist_logger.addHandler(dist_logger_handler)

        return dist_logger

    def start(self) -> None:
        """Start the node."""
        self._connect_hub()

    def _on_scenario_start(self) -> None:
        """Handle tasks to perform on experiment scenario start."""
        raise NotImplementedError

    def _on_scenario_end(self) -> None:
        """Handle tasks to perform on experiment scenario end."""
        raise NotImplementedError

    def _on_hub_connected(self) -> None:
        """Handle tasks to perform after a connection to the hub node."""
        pass

    def _on_hub_disconnected(self) -> None:
        """Handle tasks to perform after a disconnection from the hub node."""
        pass

    def _on_peer_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle a node disconnection."""
        assert peer_node_id == NODE_ID_HUB

        self.logger.warning(log_msg)

        self._on_hub_disconnected()
        self._reconnect_timer()

    def _on_hub_connect_failed(self, hub_address: str, reason: str) -> None:
        """Connection attempt to the hub failed."""
        assert hub_address == self._hub_conn.peer_address

        self.logger.warning("Connection attempt to the hub node at %s failed: %s", hub_address, reason)
        self._reconnect_timer()

    def _on_outbound_connected(self, outbound_conn_event: OutboundEvent,
                               received_node_id: int, received_node_type: int) -> None:
        """Connection attempt to the hub succeeded."""
        hub_address = self._hub_conn.peer_address
        assert outbound_conn_event.peer_addr == hub_address

        if received_node_type != NODE_TYPE_HUB:
            raise PeerResponseError(f"Connection with the hub node at {hub_address}: expected hub node type "
                                    f"{NODE_TYPE_HUB}, but received node type {received_node_type}.  Is this the hub?")

        if self.node_id == NODE_ID_UNASSIGNED:
            # first connection to the hub
            self.node_id = received_node_id
            self.logger.info("Our assigned node id is: %d", self.node_id)
        elif self.node_id != received_node_id:
            raise PeerResponseError(f"Connection with the hub node at {hub_address}: we were assigned node id "
                                    f"{self.node_id}, but received node id {received_node_id}.  Is this the hub?")

        self._add_connection(outbound_conn_event, self._hub_conn, self._on_peer_disconnection)

        self.logger.info("Connected to the hub node at %s (connection count: %d)",
                         hub_address, self._hub_conn.connection_count)

        # if there are any pending requests, these need to be resent
        for pending_request in self._hub_conn.pending_requests:
            self._hub_conn.write_data(pending_request[0])

        self._on_hub_connected()

    def _send_hub_request(self, protocol_id: int, request_data: Sequence = (), local_data: Any = None) -> None:
        """Send a network request to hub."""
        self._send_net_request(self._hub_conn, protocol_id, request_data=request_data, local_data=local_data)

    def _send_hub_request_nr(self, protocol_id: int, request_data: Sequence = ()) -> None:
        """Send a network request to hub without response.  These requests will not be cached."""
        self._send_net_request_nr(self._hub_conn, protocol_id, request_data=request_data)

    def _connect_hub(self) -> None:
        """Initiate an outbound connection attempt to the hub node."""
        self._add_outbound_connecting(self._hub_port, self._hub_conn,
                                      self._on_hub_connect_failed, self._on_outbound_connected)

        self.logger.info("Connecting to the hub node at %s, port %d ...", self._hub_conn.peer_address, self._hub_port)

    def _reconnect_timer(self):
        """Create a new timer to act as a delay for peer reconnection attempt."""
        timer_event = self._add_timer(self._handle_reconnect_timer)
        timer_event.set(self._hub_reconnect_delay)
        self.logger.info("Waiting %d seconds before reconnecting ...", self._hub_reconnect_delay)

    def _handle_reconnect_timer(self, timer_event, num_expires):
        """Handle reconnect timer expiration."""
        self._event_close(timer_event)
        # the timer should only expire once, multiple expires suggests polling loop is lagging
        self.logger.debug("Hub reconnection timer expiry count: %d", num_expires)
        self._connect_hub()

    # network request handlers
    @staticmethod
    def _handle_heartbeat(node_id: int) -> tuple:
        """Handle heartbeat from hub."""
        assert node_id == NODE_ID_HUB
        return ()

    def _handle_scenario_start(self, node_id: int) -> tuple:
        """Handle start of experiment scenario."""
        assert node_id == NODE_ID_HUB
        self.logger.info("Received experiment start notification from the hub node")
        self._on_scenario_start()
        return ()

    def _handle_scenario_stop(self, node_id: int) -> tuple:
        """Handle end of experiment scenario."""
        assert node_id == NODE_ID_HUB
        self.logger.info("Received experiment end notification from the hub node")
        self._on_scenario_end()
        return ()


class SynchronizedClientNode(ClientNode):
    """Thread safe client node base.  These nodes enable thread safe operations."""

    __slots__ = ('_task_queue', '_task_lock', '_task_counter')

    def __init__(self, system_config: Mapping, node_type: int):
        """Constructor."""
        super().__init__(system_config, node_type)

        self._task_queue: List[Tuple[Callable[..., None], Tuple[Any, ...]]] = []
        self._task_lock = threading.Lock()
        self._task_counter = self._add_counter(self._handle_tasks)

    def _on_scenario_start(self) -> None:
        """Handle tasks to perform on experiment scenario start."""
        raise NotImplementedError

    def _on_scenario_end(self) -> None:
        """Handle tasks to perform on experiment scenario end."""
        raise NotImplementedError

    def _sync_add_task(self, cb_task: Callable[..., None], *args) -> None:
        """Add a thread task to be executed in the main thread."""
        with self._task_lock:
            self._task_queue.append((cb_task, args))
            self._task_counter.increment()

    def _send_hub_request(self, protocol_id: int, request_data: Sequence = (), local_data: Any = None) -> None:
        """Add a network request to the send queue.  Synchronized."""
        self._sync_add_task(self._send_net_request, self._hub_conn, protocol_id, request_data, local_data)

    def _send_hub_request_nr(self, protocol_id: int, request_data: Sequence = ()) -> None:
        """Send a network request to hub without response.  These requests will not be cached.  Synchronized."""
        self._sync_add_task(self._send_net_request_nr, self._hub_conn, protocol_id, request_data)

    # event handlers
    def _handle_tasks(self, counter_event: CounterEvent, num_increments: int):
        """Process queued thread tasks."""
        assert threading.current_thread() is threading.main_thread()
        assert counter_event is self._task_counter

        with self._task_lock:
            current_tasks = self._task_queue
            self._task_queue = []

        for cb_task, args in current_tasks:
            cb_task(*args)

        self.logger.debug("Processed %d queued thread tasks (counter: %d)", len(current_tasks), num_increments)
