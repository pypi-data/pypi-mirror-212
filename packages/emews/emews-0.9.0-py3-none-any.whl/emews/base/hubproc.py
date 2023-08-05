"""Hub process nodes.  These nodes connect to the hub for monitoring, sending commands, etc."""
from typing import Mapping

import logging
import pickle
import sys
import threading

from emews.base.client import ClientNode, SynchronizedClientNode
from emews.base.node import ConsoleFormatter, OutboundEvent, NetProtocolID, NET_PROTOCOL, NODE_ID_HUB, \
    NODE_TYPE_HUBCONSOLE, NODE_TYPE_HUBMON, STR_ENCODING


class HubConsole(SynchronizedClientNode):
    """Provides an interface to the hub for giving commands."""

    __slots__ = ('_console_thread', '_console_event', '_console_counter', '_current_command',
                 '_prompt', '_thread_exit_counter', '_console_exit', '_console_eof')

    def __init__(self, system_config: Mapping):
        """Constructor."""
        super().__init__(system_config, NODE_TYPE_HUBCONSOLE)

        import readline  # importing this module adds command history to input()

        NET_PROTOCOL[NetProtocolID.HUB_HUBCONSOLE_WEL].response_handler = self._response_console_welcome
        NET_PROTOCOL[NetProtocolID.HUB_CONSOLE_COMMAND].response_handler = self._response_console_command

        self._console_thread = threading.Thread(name="console", target=self._console, daemon=True)

        self._console_event = threading.Event()
        self._console_counter = self._add_counter(self._handle_console_counter)
        self._thread_exit_counter = self._add_counter(self._handle_thread_exit_counter)

        self._console_exit = False
        self._console_eof = False

        self._current_command: str = ''
        self._prompt = ":>"

    def start(self) -> None:
        """Start the node."""
        self._send_hub_request(NetProtocolID.HUB_HUBCONSOLE_WEL)
        super().start()

    def shutdown(self) -> None:
        """Handle shutdown tasks post event-loop stop."""
        sys.stdout.write("\n")

    def _shutdown_signal_handler(self, signum: int, frame):
        """Signal handler for incoming signals (those which are registered)."""
        if not self._hub_conn.is_connected:
            super()._shutdown_signal_handler(signum, frame)
            return

        sys.stdout.write(f"Use CTRL-D to exit console\n{self._prompt}")
        sys.stdout.flush()

    def _on_scenario_start(self) -> None:
        pass

    def _on_scenario_end(self) -> None:
        pass

    def _connect_hub(self) -> None:
        """Initiate an outbound connection attempt to the hub node."""
        sys.stdout.write(f"Connecting to the hub node at {self._hub_conn.peer_address}, port {self._hub_port} ...\n")
        sys.stdout.flush()
        super()._connect_hub()

    def _on_peer_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle hub node disconnection."""
        sys.stdout.write(f"\nDisconnected from hub node: {log_msg}\n")
        sys.stdout.flush()
        super()._on_peer_disconnection(peer_node_id, log_msg)

    def _on_hub_connect_failed(self, hub_address: str, reason: str) -> None:
        """Connection attempt to the hub failed."""
        sys.stdout.write(f"Could not connect to the hub node: {reason}\n")
        sys.stdout.flush()
        super()._on_hub_connect_failed(hub_address, reason)

    def _reconnect_timer(self):
        """Create a new timer to act as a delay for peer reconnection attempt."""
        sys.stdout.write(f"Waiting {self._hub_reconnect_delay} seconds before trying to connect again...\n")
        sys.stdout.flush()
        super()._reconnect_timer()

    def _on_outbound_connected(self, outbound_conn_event: OutboundEvent,
                               received_node_id: int, received_node_type: int) -> None:
        """Connection attempt to the hub node succeeded."""
        super()._on_outbound_connected(outbound_conn_event, received_node_id, received_node_type)
        sys.stdout.write(f"Connected to the hub node\n\n")
        sys.stdout.flush()

    def _console(self):
        """Console thread.  Provides a console for user input."""
        while not self._console_exit:
            try:
                command = input(self._prompt)
            except EOFError:
                # ctrl-D pressed
                self._console_eof = True
                break

            command = command.strip()
            if command == '':
                continue

            self._current_command = command
            self._console_counter.increment()

            self._console_event.wait()  # wait for command to process (handle_console_counter())
            self._console_event.clear()

        self._thread_exit_counter.increment()

    # event handlers
    def _handle_console_counter(self, counter_event, num_increments):
        """Process current command (main thread execution)."""
        assert counter_event is self._console_counter
        assert num_increments == 1

        command = self._current_command

        if command.split()[0] == 'exit':
            # ignore any args that may be given with the command
            self._console_exit = True
            self._console_event.set()
            return

        # send command to hub
        self._send_hub_request(NetProtocolID.HUB_CONSOLE_COMMAND, request_data=(bytes(command, STR_ENCODING),))

    def _handle_thread_exit_counter(self, counter_event, num_increments):
        """Process console thread exit (main thread execution)."""
        assert counter_event is self._thread_exit_counter

        if self._console_eof:
            sys.stdout.write("\n\nConsole session finished (EOF)")
        else:
            sys.stdout.write("\nConsole session finished (exit)")
        sys.stdout.flush()

        self.stop()

    # net responses
    def _response_console_welcome(self, node_id: int, local_data, hub_name: bytes, welcome_msg: bytes):
        """Response from hub node for welcome msg."""
        assert node_id == NODE_ID_HUB

        self._prompt = f"{ConsoleFormatter.STYLE_BOLD}{self.node_name}@{hub_name.decode()}" \
                       f"{self._prompt}{ConsoleFormatter.STYLE_ENDC} "

        sys.stdout.write(f"{welcome_msg.decode()}\n\n")
        sys.stdout.write("Type 'exit' to exit console.\n")
        sys.stdout.flush()
        self._console_thread.start()

    def _response_console_command(self, node_id: int, local_data, cmd_result: bytes):
        """Response from hub to command issued."""
        assert node_id == NODE_ID_HUB

        sys.stdout.write(cmd_result.decode())
        sys.stdout.flush()

        self._console_event.set()


class HubMon(ClientNode):
    """Provides an interface to the hub for monitoring."""

    __slots__ = ('logger_in_dist',)

    def __init__(self, system_config: Mapping):
        """Constructor."""
        super().__init__(system_config, NODE_TYPE_HUBMON)

        NET_PROTOCOL[NetProtocolID.HUBMON_LOGGING_MESSAGE].request_handler = self._handle_logging_message

        log_config = system_config['logging']

        stream_path, stream_name = log_config['log_stream'].rsplit(".", 1)
        in_dist_log_handler = logging.StreamHandler(
            stream=getattr(sys.modules[stream_path], stream_name))
        in_dist_log_handler.setLevel(log_config['log_message_level'])
        in_dist_log_handler.setFormatter(ConsoleFormatter(log_config['log_message_format_dist']))

        in_dist_logger = logging.getLogger("emews_monitor_in_dist")
        in_dist_logger.setLevel(logging.DEBUG)
        in_dist_logger.propagate = False  # don't propagate messages up to (logging) root
        in_dist_logger.addHandler(in_dist_log_handler)

        self.logger_in_dist = in_dist_logger

    def _on_scenario_start(self) -> None:
        pass

    def _on_scenario_end(self) -> None:
        pass

    def _connect_hub(self) -> None:
        """Initiate an outbound connection attempt to the hub node."""
        sys.stdout.write(f"Connecting to the hub node at {self._hub_conn.peer_address}, port {self._hub_port} ...\n")
        sys.stdout.flush()
        super()._connect_hub()

    def _on_peer_disconnection(self, peer_node_id: int, log_msg: str) -> None:
        """Handle hub node disconnection."""
        sys.stdout.write(f"\n{ConsoleFormatter.STYLE_WARNING}Disconnected from hub node: "
                         f"{log_msg}{ConsoleFormatter.STYLE_ENDC}\n")
        sys.stdout.flush()
        super()._on_peer_disconnection(peer_node_id, log_msg)

    def _on_hub_connect_failed(self, hub_address: str, reason: str) -> None:
        """Connection attempt to the hub failed."""
        sys.stdout.write(f"{ConsoleFormatter.STYLE_WARNING}Could not connect to the hub node: "
                         f"{reason}{ConsoleFormatter.STYLE_ENDC}\n")
        sys.stdout.flush()
        super()._on_hub_connect_failed(hub_address, reason)

    def _reconnect_timer(self):
        """Create a new timer to act as a delay for peer reconnection attempt."""
        sys.stdout.write(f"Waiting {self._hub_reconnect_delay} seconds before trying to connect again...\n")
        sys.stdout.flush()
        super()._reconnect_timer()

    def _on_outbound_connected(self, outbound_conn_event: OutboundEvent,
                               received_node_id: int, received_node_type: int) -> None:
        """Connection attempt to the hub node succeeded."""
        super()._on_outbound_connected(outbound_conn_event, received_node_id, received_node_type)
        sys.stdout.write(f"Connected to the hub node\n\n")
        sys.stdout.flush()

    def _handle_logging_message(self, node_id: int, src_node_id: int, src_node_name: bytes, log_msg: bytes) -> None:
        """Process the log message.  Log messages could be from any node connected to the hub."""
        assert node_id == NODE_ID_HUB

        d = pickle.loads(log_msg)
        d['args'] = None  # needed so getMessage() will not process args again
        d['exc_info'] = None  # needed so format() will not cache trace info again
        d['node_id'] = src_node_id
        d['node_name'] = src_node_name.decode()

        self.logger_in_dist.handle(logging.makeLogRecord(d))
