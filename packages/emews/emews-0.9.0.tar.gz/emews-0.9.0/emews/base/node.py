"""Node module."""
from typing import Any, Callable, Deque, Dict, List, Mapping, Protocol, Sequence, Tuple, Union

import collections
import importlib
import logging
import os
import pickle
import select
import signal
import socket
import struct
import sys


from linuxfd import eventfd, timerfd

from emews.__about__ import __version__
from emews.base.config import parse_system_config


# typing hint aliases
class SendRequestCB(Protocol):
    def __call__(self, conn_state: 'ConnectionState', protocol_id: int,
                 request_data: Sequence = (), local_data: Any = None) -> None:
        pass


NetworkRequestCB = Callable[..., Tuple]
NetworkResponseCB = Callable[..., None]
InboundConnectedCB = Callable[['InboundEvent', str, int, int], None]
OutboundConnectedCB = Callable[['OutboundEvent', int, int], None]
InboundAcceptCB = Callable[[socket.socket, str, InboundConnectedCB], None]
ConnectFailedCB = Callable[[str, str], None]
DisconnectionCB = Callable[[int, str], None]
TimerEventCB = Callable[['TimerEvent', int], None]
CounterEventCB = Callable[['CounterEvent', int], None]
PollingUpdateCB = Callable[['PollEvent', int], None]
EventCloseCB = Callable[['PollEvent'], None]

STR_ENCODING = 'utf_8'

NET_CATEGORY_REQUEST = 0   # net requests
NET_CATEGORY_RESPONSE = 1  # net responses

NODE_ID_UNASSIGNED = 0
NODE_ID_HUB = 1

NODE_TYPE_HUB = 0
NODE_TYPE_HOST = 1
NODE_TYPE_HOSTPROC = 2
NODE_TYPE_HUBMON = 3
NODE_TYPE_HUBCONSOLE = 4

NAME_STR_NODE_TYPE = {
    NODE_TYPE_HUB: 'hub',
    NODE_TYPE_HOST: 'host',
    NODE_TYPE_HOSTPROC: 'host_process',
    NODE_TYPE_HUBMON: 'monitor',
    NODE_TYPE_HUBCONSOLE: 'console',
}


class NetworkRequestError(Exception):
    """Raised when a network request cannot complete (external to handler errors)."""
    def __init__(self, req_num: int, *args):
        """Constructor."""
        super().__init__(*args)
        self.req_num = req_num

    def __str__(self):
        """"Return str(self)."""
        return f"{super().__str__()} (req num={self.req_num})"


class NetworkHandlerError(Exception):
    """Raised in a network handler cannot complete a task (request or response)."""
    pass


class PollEventError(Exception):
    """Raised when an event raises an error (usually read or write OSError)."""
    pass


class PeerResponseError(Exception):
    """Raised when received NACK from a peer."""
    pass


class NoConnectionError(Exception):
    """Raised when an operation is attempted that requires a connection."""
    pass


# mapping of supported protocol action types and their size (in bytes)
TYPE_LEN = {
    'b': 1,  # boolean, '?' in struct
    'B': 1,  # boolean, '?' in struct
    '?': 1,  # boolean struct type (same as 'b' and 'B', as these get converted to boolean)
    'h': 2,
    'H': 2,
    'i': 4,
    'I': 4,
    'l': 4,
    'L': 4,
    'f': 4,
    'q': 8,
    'Q': 8,
    'd': 8,
    's': 4,  # bytestring, denotes the size of 'L', which gives the size of the string len
}


class NetProtocol:
    """
    Specification for a networking protocol.

    Protocol objects are used by networking clients to send properly-formatted data
    to respective environments, and anticipate the response types from the server.

    The bytes type ('s') can be used with strings if the strings are encoded as bytes first, and
    can also be used as an arbitrary format by passing structs.

    Current prefix format: LHHL (total_len + net_category + protocol_id + req_num)
    total_len = prefix len + payload len
    """

    class NetStruct:
        """Struct data related to a request or a response."""

        __slots__ = ('struct_prefix', 'struct_fmt_pack', 'struct_fmt_unpack')

        def __init__(self, protocol_id: int, net_category: int, payload_len: int,
                     payload_types: str):
            """Constructor."""
            # payload is known and can be included in the prefix
            total_len = TYPE_LEN['H'] + TYPE_LEN['H'] + TYPE_LEN['L'] + payload_len
            self.struct_prefix = struct.pack('>LHH', total_len, net_category, protocol_id)
            # prefix struct (bytes) + req_num (int) + payload types
            self.struct_fmt_pack = f">{len(self.struct_prefix)}sL{payload_types}"
            self.struct_fmt_unpack = f">{payload_types}"

        def pack_data(self, req_num: int, data_vals: Sequence) -> bytes:
            """Pack the data."""
            return struct.pack(self.struct_fmt_pack, self.struct_prefix, req_num, *data_vals)

        def unpack_data(self, byte_buffer: bytearray, offset: int) -> tuple:
            """Unpack struct from buffer at given offset."""
            return struct.unpack_from(self.struct_fmt_unpack, byte_buffer, offset=offset)

    class NRNetStruct:
        """Struct data for a protocol that does not have request and/or response data."""

        __slots__ = ('struct_prefix', 'struct_fmt_pack')

        def __init__(self, protocol_id: int, net_category: int):
            """Constructor."""
            total_len = TYPE_LEN['H'] + TYPE_LEN['H'] + TYPE_LEN['L']  # category, protocol, req_num
            self.struct_prefix = struct.pack('>LHH', total_len, net_category, protocol_id)
            # prefix struct (bytes) + req_num (int)
            self.struct_fmt_pack = f">{len(self.struct_prefix)}sL"

        def pack_data(self, req_num: int, data_vals: Sequence) -> bytes:
            """Pack the data."""
            # data_vals is ignored here, as it should be empty
            return struct.pack(self.struct_fmt_pack, self.struct_prefix, req_num)

        @staticmethod
        def unpack_data(byte_buffer: bytearray, offset: int) -> tuple:
            """Unpack struct from buffer at given offset."""
            # there is no payload to unpack; this method serves as a placeholder with compatible signature
            return ()

    class BNetStruct:
        """Struct data related to a request or a response, supporting bytes type."""

        __slots__ = ('struct_prefix', 's_indices', 'partial_len', 'struct_fmt_pack',
                     'struct_fmt_unpack', 'struct_fmt_s', 's_offset')

        def __init__(self, protocol_id: int, net_category: int, payload_len: int,
                     payload_types: str, s_indices: Sequence[int]):
            """Constructor."""
            self.s_indices = s_indices  # indices of bytes types
            # payload len is not fully known, as bytes types (s-type) are variable length
            # payload len is a sum of all non-s types + sizeof variables for s-type lens
            self.partial_len = TYPE_LEN['H'] + TYPE_LEN['H'] + TYPE_LEN['L'] + payload_len
            # prefix excludes the total_len (not fully known)
            self.struct_prefix = struct.pack('>HH', net_category, protocol_id)

            struct_fmt_s = 'L' * len(s_indices)  # len of vars holding bytes types lens

            # total_len + prefix struct (bytes) + req_num (int) + bytes_len + payload types
            self.struct_fmt_pack = f">L{len(self.struct_prefix)}sL{struct_fmt_s}{payload_types}"
            self.struct_fmt_unpack = f">{payload_types}"
            self.struct_fmt_s = f">{struct_fmt_s}"  # unpack bytes types
            self.s_offset = TYPE_LEN['L'] * len(s_indices)

        def pack_data(self, req_num: int, data_vals: Sequence) -> bytes:
            """Pack the data."""
            s_lens = [len(data_vals[s_index]) for s_index in self.s_indices]
            tot_len = self.partial_len + sum(s_lens)

            return struct.pack(self.struct_fmt_pack.format(*s_lens), tot_len, self.struct_prefix,
                               req_num, *s_lens, *data_vals)

        def unpack_data(self, byte_buffer: bytearray, offset: int) -> tuple:
            """Unpack struct from buffer at given offset."""
            f_unpack = struct.unpack_from
            s_lens = f_unpack(self.struct_fmt_s, byte_buffer, offset=offset)

            return f_unpack(self.struct_fmt_unpack.format(*s_lens), byte_buffer, offset=offset+self.s_offset)

    __slots__ = ('protocol_id', 'pack_request', 'unpack_request', 'pack_response', 'unpack_response',
                 'request_handler', 'response_handler')

    def __init__(self, protocol_id: int, request_types: Union[Sequence, None], response_types: Union[Sequence, None]):
        """Constructor."""
        self.protocol_id = protocol_id

        if request_types is None:
            request = NetProtocol.NRNetStruct(protocol_id, NET_CATEGORY_REQUEST)
        else:
            request = self._build_fmt(NET_CATEGORY_REQUEST, request_types)

        self.pack_request = request.pack_data
        self.unpack_request = request.unpack_data
        self.request_handler: NetworkRequestCB = self.unassigned_request_handler

        if response_types is None:
            response = NetProtocol.NRNetStruct(protocol_id, NET_CATEGORY_RESPONSE)
            self.response_handler: NetworkResponseCB = self.no_response_handler
        else:
            response = self._build_fmt(NET_CATEGORY_RESPONSE, response_types)
            self.response_handler: NetworkResponseCB = self.unassigned_response_handler

        self.pack_response = response.pack_data
        self.unpack_response = response.unpack_data

    def no_response_handler(self, node_id: int, local_data: Any, *args) -> None:
        """Network response handler.  Optionally assigned to handle responses with data from this protocol."""
        pass

    def unassigned_request_handler(self, node_id: int, *args) -> tuple:
        """Network request handler.  Must be assigned to handle request from this protocol."""
        raise NetworkHandlerError(f"protocol {self.protocol_id} does not have a request handler assigned")

    def unassigned_response_handler(self, node_id: int, local_data: Any, *args) -> None:
        """Network response handler.  Optionally assigned to handle responses with data from this protocol."""
        raise NetworkHandlerError(f"protocol {self.protocol_id} does not have a response handler assigned")

    def _build_fmt(self, net_category: int, data_types: Sequence):
        data_fmt = []
        s_type_indices: List[int] = []  # string lengths (one per string)
        fmt_len = 0  # payload len (minus string lengths as those are unknown)

        for chr_index, fmt_chr in zip(range(len(data_types)), data_types):
            if fmt_chr == 's':
                # strings require a length
                data_fmt.append('{}')  # used as format string to fill in length once known
                s_type_indices.append(chr_index)  # idx of s-type (bytes type)
            elif fmt_chr == 'B' or fmt_chr == 'b':
                # boolean types
                fmt_chr = '?'  # boolean type char in struct for boolean type

            data_fmt.append(fmt_chr)
            fmt_len += TYPE_LEN[fmt_chr]

        type_str = "".join(data_fmt)

        if len(s_type_indices):
            # bytes types present
            net_data = NetProtocol.BNetStruct(self.protocol_id, net_category, fmt_len, type_str,
                                              s_type_indices)
        else:
            # no s types
            net_data = NetProtocol.NetStruct(self.protocol_id, net_category, fmt_len, type_str)

        return net_data


# protocol definitions
class NetProtocolID:
    """Network protocol IDs."""
    CLIENT_HEARTBEAT = 2
    CLIENT_SCENARIO_START = 70
    CLIENT_SCENARIO_STOP = 71

    HUB_HUBCONSOLE_WEL = 108
    HUB_LOGGING_MESSAGE = 110
    HUB_SERVICE_REG = 120
    HUB_SERVICE_SEND_ALL = 130
    HUB_SERVICE_SEND_TO = 131
    HUB_SERVICE_TELL = 132
    HUB_SERVICE_ASK = 133
    HUB_SERVICE_ENVKEY_ID = 134
    HUB_SERVICE_STARTED = 140
    HUB_SERVICE_STOPPED = 141
    HUB_SERVICE_SPAWNED = 142
    HUB_SERVICE_EXITED = 143
    HUB_CONSOLE_COMMAND = 150

    HOST_SERVICE_SEND_MSG = 172
    HOST_SERVICE_LOCAL_REQ = 173  # from hostproc - service spawn request
    HOST_SERVICE_SPAWN = 174  # from hub service - spawn request
    HOST_SERVICE_START = 175
    HOST_SERVICE_STOP = 176

    HUBMON_LOGGING_MESSAGE = 210


NET_PROTOCOL = {
    # request: none
    # response: none
    NetProtocolID.CLIENT_HEARTBEAT: NetProtocol(
        NetProtocolID.CLIENT_HEARTBEAT, None, None),
    # request: none
    # response: hub name, welcome msg
    NetProtocolID.HUB_HUBCONSOLE_WEL: NetProtocol(
        NetProtocolID.HUB_HUBCONSOLE_WEL, None, ['s', 's']),
    # request: args (command, command args)
    # response: command result
    NetProtocolID.HUB_CONSOLE_COMMAND: NetProtocol(
        NetProtocolID.HUB_CONSOLE_COMMAND, ['s'], ['s']),
    # request: levelno, log message
    # response: none
    NetProtocolID.HUB_LOGGING_MESSAGE: NetProtocol(
        NetProtocolID.HUB_LOGGING_MESSAGE, ['H', 's'], None),
    # request: service name, service config filename
    # response: service instance id, service display name
    NetProtocolID.HUB_SERVICE_REG: NetProtocol(
        NetProtocolID.HUB_SERVICE_REG, ['s', 's'], ['L', 's']),
    # request: from service instance id, data
    # response: none
    NetProtocolID.HUB_SERVICE_SEND_ALL: NetProtocol(
        NetProtocolID.HUB_SERVICE_SEND_ALL, ['L', 's'], None),
    # request: from service instance id, to services, data
    # response: none
    NetProtocolID.HUB_SERVICE_SEND_TO: NetProtocol(
        NetProtocolID.HUB_SERVICE_SEND_TO, ['L', 's', 's'], None),
    # request: service instance id, observation key id, observation value
    # response: None
    NetProtocolID.HUB_SERVICE_TELL: NetProtocol(
        NetProtocolID.HUB_SERVICE_TELL, ['L', 'H', 's'], None),
    # request: service instance id, evidence key id
    # response: evidence
    NetProtocolID.HUB_SERVICE_ASK: NetProtocol(
        NetProtocolID.HUB_SERVICE_ASK, ['L', 'H'], ['s']),
    # request: environment key full name
    # response: environment key id
    NetProtocolID.HUB_SERVICE_ENVKEY_ID: NetProtocol(
        NetProtocolID.HUB_SERVICE_ENVKEY_ID, ['s'], ['H']),
    # request: service instance id
    # response: none
    NetProtocolID.HUB_SERVICE_STARTED: NetProtocol(
        NetProtocolID.HUB_SERVICE_STARTED, ['L'], None),
    # request: service instance id
    # response: none
    NetProtocolID.HUB_SERVICE_STOPPED: NetProtocol(
        NetProtocolID.HUB_SERVICE_STOPPED, ['L'], None),
    # request: service instance id, is instantiated
    # response: None
    NetProtocolID.HUB_SERVICE_SPAWNED: NetProtocol(
        NetProtocolID.HUB_SERVICE_SPAWNED, ['L', 'B'], None),
    # request: service instance id, is failed
    # response: none
    NetProtocolID.HUB_SERVICE_EXITED: NetProtocol(
        NetProtocolID.HUB_SERVICE_EXITED, ['L', 'B'], None),
    # request: none
    # response: none
    NetProtocolID.CLIENT_SCENARIO_START: NetProtocol(
        NetProtocolID.CLIENT_SCENARIO_START, None, None),
    # request: none
    # response: none
    NetProtocolID.CLIENT_SCENARIO_STOP: NetProtocol(
        NetProtocolID.CLIENT_SCENARIO_STOP, None, None),
    # request: from service instance id, to service instance id, data
    # response: none
    NetProtocolID.HOST_SERVICE_SEND_MSG: NetProtocol(
        NetProtocolID.HOST_SERVICE_SEND_MSG, ['L', 'L', 's'], None),
    # request: service name, service config file name
    # response: none
    NetProtocolID.HOST_SERVICE_LOCAL_REQ: NetProtocol(
        NetProtocolID.HOST_SERVICE_LOCAL_REQ, ['s', 's'], None),
    # request: service name, config filename, service instance id, service display name
    # response: none
    NetProtocolID.HOST_SERVICE_SPAWN: NetProtocol(
        NetProtocolID.HOST_SERVICE_SPAWN, ['s', 's', 'L', 's'], None),
    # request: service instance id
    # response: none
    NetProtocolID.HOST_SERVICE_START: NetProtocol(
        NetProtocolID.HOST_SERVICE_START, ['L'], None),
    # request: service instance id
    # response: none
    NetProtocolID.HOST_SERVICE_STOP: NetProtocol(
        NetProtocolID.HOST_SERVICE_STOP, ['L'], None),
    # request: node id, node name, log message
    # response: none
    NetProtocolID.HUBMON_LOGGING_MESSAGE: NetProtocol(
        NetProtocolID.HUBMON_LOGGING_MESSAGE, ['L', 's', 's'], None),
}


class ConsoleFormatter(logging.Formatter):
    """Formatter which applies console styling to log message."""

    # color codes adapted from the Blender bcolors.py module:
    # https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    STYLE_BOLD = "\033[1m"
    STYLE_HEADER = "\033[95m"
    STYLE_OKBLUE = "\033[94m"
    STYLE_INFOGREEN = "\033[32m"
    STYLE_WARNING = "\033[33m"
    STYLE_FAIL = "\033[91m"
    STYLE_ENDC = "\033[0m"

    STYLE_MAP = {
        logging.WARNING: STYLE_WARNING,
        logging.WARN: STYLE_WARNING,
        logging.ERROR: STYLE_FAIL,
        logging.FATAL: STYLE_FAIL,
        logging.CRITICAL: STYLE_FAIL
    }

    def format(self, record):
        """@Override format the log record."""
        msg = super().format(record)
        if record.levelno in ConsoleFormatter.STYLE_MAP:
            # a vast majority of log messages will be DEBUG or INFO
            return f"{ConsoleFormatter.STYLE_MAP[record.levelno]}{msg}{ConsoleFormatter.STYLE_ENDC}"

        return msg


def log_record_make_pickle(record: logging.LogRecord, formatter: Callable[[logging.LogRecord], str]) -> bytes:
    """
    Convert a log record to bytes (pickled).

    Pickling code adapted from logging.Handlers.SocketHandler.makePickle() - current as of
    Python 3.9.1.  Note, pickle.dumps() still uses protocol 1 in SocketHandler.  eMews uses the default protocol,
    currently 4.
    """
    if record.exc_info:
        # calling format will write traceback text to record.exc_text
        formatter(record)

    d = dict(record.__dict__)
    d['msg'] = record.getMessage()  # merges any args to log msg and returns a string

    # pop keys we don't need for message reconstruction
    d.pop('args', None)  # args merged into msg
    d.pop('exc_info', None)  # if present, converted to a string and in d['exc_text']
    d.pop('message', None)  # Issue #25685: delete 'message' if present: redundant with 'msg'

    return pickle.dumps(d)


class PollEvent:
    """Base class for polling events.  Provides a wrapper for file descriptor objects."""
    POLL_ERR = select.POLLHUP | select.POLLERR
    POLL_RO = select.POLLIN | select.POLLPRI | POLL_ERR
    POLL_RW = POLL_RO | select.POLLOUT
    POLL_WO = select.POLLOUT | POLL_ERR

    __slots__ = ('_res', '_fd')

    def __init__(self, res_obj):
        """Constructor."""
        self._res = res_obj  # resource (assumed to have fileno() and close() methods)
        self._fd = res_obj.fileno()

    def fileno(self) -> int:
        """Return the resource file descriptor."""
        return self._fd

    def close(self) -> None:
        """Close event resource."""
        self._res.close()

    def close_unexpected(self, reason: str) -> None:
        """Close the event resource unexpectedly."""
        self.close()
        raise PollEventError("Event with fd '%d' closed unexpectedly: %s", self.fileno(), reason)

    def process(self, event_flag: int) -> None:
        """process the poll events."""
        raise NotImplementedError


class ListenerEvent(PollEvent):
    """Socket event for listener sockets."""

    __slots__ = ('_on_listener_accept', '_on_connected_inbound')

    def __init__(self, port: int, on_listener_accept: InboundAcceptCB,
                 on_connected_inbound: InboundConnectedCB):
        """Constructor."""
        serv_sock = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)
        serv_sock.setblocking(False)

        super().__init__(serv_sock)

        self._on_listener_accept = on_listener_accept
        self._on_connected_inbound = on_connected_inbound

        try:
            serv_sock.bind(('', port))
            serv_sock.listen(5)
        except OSError:
            serv_sock.close()
            raise

    def process(self, event_flag: int) -> None:
        """Pass socket and other information to the inbound connection callback."""
        assert event_flag & select.POLLIN  # listener socket only polls on read

        acc_sock, src_addr = self._res.accept()  # Not sure if OSError can be thrown here ...
        acc_sock.setblocking(False)

        self._on_listener_accept(acc_sock, src_addr[0], self._on_connected_inbound)


class SocketEvent(PollEvent):
    """Base class for socket_based events."""

    __slots__ = ('_expected_bytes', '_buf_in', '_buf_out', 'polling_mode',
                 '_on_polling_mode_update')

    def __init__(self, sock: socket.socket, expected_bytes: int, polling_mode: int,
                 on_polling_mode_update: PollingUpdateCB):
        """constructor."""
        super().__init__(sock)

        self._expected_bytes = expected_bytes  # expected bytes to receive on socket
        self.polling_mode = polling_mode
        self._on_polling_mode_update = on_polling_mode_update

        self._buf_in = bytearray()  # recv buffer
        self._buf_out = bytearray()  # send buffer

    def on_recv_data(self) -> int:
        """All expected bytes received."""
        raise NotImplementedError

    def write_data(self, packed_data: bytes) -> None:
        """Write packed data to out buffer for sending."""
        self._buf_out.extend(packed_data)
        if self.polling_mode != PollEvent.POLL_RW:
            self.polling_mode = PollEvent.POLL_RW
            self._on_polling_mode_update(self, PollEvent.POLL_RW)

    def process(self, event_flag: int) -> None:
        """Read data from and/or write to the socket."""
        if event_flag & (select.POLLIN | select.POLLPRI):
            # read from socket
            try:
                chunk = self._res.recv(self._expected_bytes)
            except (ConnectionError, TimeoutError) as ex:
                raise PollEventError(ex)

            if not chunk:
                # zero length chunk, stream probably closed
                raise PollEventError("connection reset by peer - on recv")

            self._buf_in.extend(chunk)

            if len(chunk) < self._expected_bytes:
                # num bytes recv is less than what is expected.
                self._expected_bytes = self._expected_bytes - len(chunk)
            else:
                # received all expected bytes
                self._expected_bytes = self.on_recv_data()
                self._buf_in.clear()

        if event_flag & select.POLLOUT:
            # write to the socket
            try:
                bytes_sent = self._res.send(self._buf_out)
            except ConnectionError as ex:
                raise PollEventError(ex)

            if bytes_sent == 0:
                # lazy socket sent nothing, connection probably closed
                raise PollEventError("connection reset by peer - on send")

            del self._buf_out[:bytes_sent]
            if not len(self._buf_out):
                # all bytes sent (buffer empty)
                self.polling_mode = PollEvent.POLL_RO
                self._on_polling_mode_update(self, PollEvent.POLL_RO)


class OutboundEvent(SocketEvent):
    """Socket event - outbound connection attempt to a peer."""

    BYTES_CONNECTED = TYPE_LEN['L'] + TYPE_LEN['H']  # node id + node type
    BYTES_PAYLOAD_PREFIX = TYPE_LEN['H'] + TYPE_LEN['L']  # node type + num connections

    __slots__ = ('node_name', 'node_type', 'num_conn', 'peer_addr', '_is_connected', '_on_connect_failed',
                 '_on_connected_outbound')

    def __init__(self, node_name: str, node_type: int, num_conn: int, peer_addr: str, port: int,
                 on_connect_failed: ConnectFailedCB, on_connected_outbound: OutboundConnectedCB,
                 on_polling_mode_update: PollingUpdateCB):
        """Constructor."""
        new_sock = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)
        new_sock.setblocking(False)

        super().__init__(new_sock, OutboundEvent.BYTES_CONNECTED, PollEvent.POLL_WO, on_polling_mode_update)

        self.node_name = node_name
        self.node_type = node_type
        self.num_conn = num_conn
        self.peer_addr = peer_addr

        self._on_connect_failed = on_connect_failed
        self._on_connected_outbound = on_connected_outbound

        self._is_connected = False  # connection status will come when socket is writable

        new_sock.connect_ex((self.peer_addr, port))

    @property
    def sock(self):
        """Return the socket."""
        return self._res

    def close_unexpected(self, reason):
        """Socket closed unexpectedly."""
        self.close()
        self._on_connect_failed(self.peer_addr, reason)

    def process(self, event_flag: int) -> None:
        """Handle connection establishment, identity send, and reply."""
        if not self._is_connected:
            assert event_flag & PollEvent.POLL_WO

            self._is_connected = True
            conn_result = self._res.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if conn_result != 0:
                # some error occurred, connection failed
                raise PollEventError(f"connection attempt failed - {os.strerror(conn_result)}")

            str_len = len(self.node_name)
            self.write_data(struct.pack(f'>LHL{str_len}s', OutboundEvent.BYTES_PAYLOAD_PREFIX + str_len,
                                        self.node_type, self.num_conn, bytes(self.node_name, 'utf-8')))
            return

        # connected to peer
        super().process(event_flag)

    def on_recv_data(self) -> int:
        """Received node id and node type from peer."""
        received_node_id, received_node_type = struct.unpack('>LH', self._buf_in)
        self._on_connected_outbound(self, received_node_id, received_node_type)
        return 0  # event should be closed on cb


class InboundEvent(SocketEvent):
    """Socket event - inbound connection from a peer."""

    BYTES_CONNECTING = TYPE_LEN['L']  # payload len (payload is node type and node name)

    __slots__ = ('peer_addr', '_node_name_len', '_on_connect_failed', '_on_connected_inbound')

    def __init__(self, sock: socket.socket, peer_addr: str, on_connect_failed: ConnectFailedCB,
                 on_connected_inbound: InboundConnectedCB, on_polling_mode_update: PollingUpdateCB):
        """Constructor."""
        super().__init__(sock, InboundEvent.BYTES_CONNECTING, PollEvent.POLL_RO,
                         on_polling_mode_update)
        self.peer_addr = peer_addr
        self._on_connect_failed = on_connect_failed
        self._on_connected_inbound = on_connected_inbound

        self._node_name_len = None

    @property
    def sock(self):
        """Return the socket."""
        return self._res

    def close_unexpected(self, reason):
        """Socket closed unexpectedly."""
        self.close()
        self._on_connect_failed(self.peer_addr, reason)

    def on_recv_data(self) -> int:
        """Process data read by socket."""
        if self._node_name_len is None:
            payload_len = struct.unpack('>L', self._buf_in)[0]
            self._node_name_len = payload_len - OutboundEvent.BYTES_PAYLOAD_PREFIX
            return payload_len

        # received node type and node name
        recv_node_type, num_conn, recv_node_name = struct.unpack(f'>HL{self._node_name_len}s', self._buf_in)
        self._on_connected_inbound(self, recv_node_name.decode(), recv_node_type, num_conn)
        return 0  # event should be closed on cb


class ConnectionEvent(SocketEvent):
    """Socket event - connected to peer."""
    # incoming request length (total request length)
    BYTES_INCOMING_REQUEST = TYPE_LEN['L']
    # request prefix (incoming type + protocol id + req num)
    REQUEST_PREFIX = TYPE_LEN['H'] + TYPE_LEN['H'] + TYPE_LEN['L']

    __slots__ = ('logger', '_log_prefix', '_conn_state', '_awaiting', '_on_disconnection')

    def __init__(self, logger, sock: socket.socket, conn_state: 'ConnectionState',
                 on_disconnection: DisconnectionCB, on_polling_mode_update: PollingUpdateCB):
        """Constructor."""
        super().__init__(sock, ConnectionEvent.BYTES_INCOMING_REQUEST, PollEvent.POLL_RO,
                         on_polling_mode_update)

        self.logger = logger
        self._log_prefix = f"Connection with node {conn_state.peer_node_id} at "\
                           f"{conn_state.peer_address} (type={conn_state.peer_node_type}):"

        conn_state.assign_event(self)
        self._conn_state = conn_state

        self._awaiting = True  # True when waiting for a new request

        self._on_disconnection = on_disconnection

    def close(self):
        """Close socket."""
        super().close()
        self._conn_state.unassign_event()

    def close_unexpected(self, reason):
        """Close the file descriptor unexpectedly."""
        self.close()
        self._on_disconnection(self._conn_state.peer_node_id, f"{self._log_prefix} {reason}")

    def on_recv_data(self) -> int:
        """Process data read by socket."""
        if self._awaiting:
            # this is a new incoming request (payload length read)
            expected_bytes = struct.unpack('>L', self._buf_in)[0]

            self.logger.debug("%s awaiting incoming request of %d bytes ...", self._log_prefix, expected_bytes)

            self._awaiting = False
            return expected_bytes  # this will initiate a new incoming request of expected bytes length

        # incoming request received
        net_category, protocol_id, req_num, = struct.unpack_from('>HHL', self._buf_in)

        try:
            protocol_obj = NET_PROTOCOL[protocol_id]
        except KeyError as ex:
            if protocol_id == 0 and net_category == NET_CATEGORY_RESPONSE:
                raise PeerResponseError(f"{self._log_prefix} got NACK response from peer (req num={req_num})") from ex

            raise NetworkRequestError(
                req_num, f"{self._log_prefix} unknown network protocol with id {protocol_id}") from ex

        # handle by network category
        if net_category == NET_CATEGORY_REQUEST:
            ######################
            # handle peer request
            ######################
            self.logger.debug("%s received network request: protocol id: %d (req num=%d)",
                              self._log_prefix, protocol_id, req_num)

            try:
                request_data = protocol_obj.unpack_request(self._buf_in, ConnectionEvent.REQUEST_PREFIX)
            except struct.error as ex:
                raise NetworkRequestError(req_num, f"{self._log_prefix} while unpacking request data: {ex}") from ex

            try:
                response_data = protocol_obj.request_handler(self._conn_state.peer_node_id, *request_data)
            except NetworkHandlerError as ex:
                raise NetworkRequestError(req_num, f"{self._log_prefix} request handler error: {ex}") from ex

            if req_num > 0:
                # req_num = 0 signifies that the request does not want a response sent back
                self.write_data(protocol_obj.pack_response(req_num, response_data))

        elif net_category == NET_CATEGORY_RESPONSE:
            ######################
            # handle peer response
            ######################
            self.logger.debug("%s received network response: protocol id: %d (req num=%d)",
                              self._log_prefix, protocol_id, req_num)

            try:
                response_data = protocol_obj.unpack_response(self._buf_in, ConnectionEvent.REQUEST_PREFIX)
            except struct.error as ex:
                raise NetworkRequestError(req_num, f"{self._log_prefix} while unpacking response data: {ex}") from ex

            _, pending_req_num, pending_local_data = self._conn_state.pending_requests.popleft()

            if req_num != pending_req_num:
                raise NetworkRequestError(
                    req_num, f"{self._log_prefix} network request number {req_num} received from peer different from "
                             f"expected network request number {pending_req_num}")

            try:
                protocol_obj.response_handler(self._conn_state.peer_node_id, pending_local_data, *response_data)
            except NetworkHandlerError as ex:
                raise NetworkRequestError(req_num, f"{self._log_prefix} response handler error: {ex}") from ex

        else:
            raise NetworkRequestError(
                req_num, f"{self._log_prefix} unknown network request type with id {net_category}")

        # prepare for new incoming request
        self._awaiting = True
        return ConnectionEvent.BYTES_INCOMING_REQUEST


class LocalConnectionEvent(ConnectionEvent):
    """Connection event with local peer."""

    def __init__(self, logger, sock, conn_state, on_disconnection, on_polling_mode_update):
        """Constructor."""
        super().__init__(logger, sock, conn_state, on_disconnection, on_polling_mode_update)

        self._log_prefix = f"Local connection at {conn_state.peer_address} "\
                           f"(type={conn_state.peer_node_type}):"


class CounterEvent(PollEvent):
    """Counter (event_fd) event."""

    __slots__ = ('_event', '_on_increment')

    def __init__(self, on_increment: CounterEventCB):
        """Constructor."""
        self._event = eventfd(nonBlocking=True)
        super().__init__(self._event)

        self._on_increment = on_increment

    def process(self, event_flag: int) -> None:
        """Read total number of increments since last read."""
        assert event_flag & select.POLLIN  # counter only polls on read

        try:
            value = self._event.read()
        except OSError as ex:
            raise PollEventError(ex)

        self._on_increment(self, value)

    def increment(self) -> None:
        """Increment the counter by one."""
        self._event.write()


class TimerEvent(PollEvent):
    """Timer event."""

    __slots__ = ('_timer', '_on_timer_expiry')

    def __init__(self, on_timer_expiry: TimerEventCB):
        """Constructor."""
        self._timer = timerfd(nonBlocking=True)
        super().__init__(self._timer)

        self._on_timer_expiry = on_timer_expiry

    def process(self, event_flag: int) -> None:
        """Timer expired.  Number of expirations given."""
        assert event_flag & select.POLLIN  # timer only polls on read

        try:
            value = self._timer.read()
        except OSError as ex:
            raise PollEventError(ex)

        self._on_timer_expiry(self, value)

    def set(self, time: int, repeat=False) -> None:
        """Set the timer, according to time (seconds).  If repeat, timer expires on an interval."""
        if repeat:
            self._timer.settime(value=time, interval=time)
        else:
            # only expire once
            self._timer.settime(value=time)


class ConnectionState:
    """Persistent connection state."""
    __slots__ = ('peer_node_id', 'peer_node_type', 'peer_address', 'pending_requests', 'connection_count',
                 '_conn_event', '_conn_event_write', '_free_req_num')

    def __init__(self, peer_node_id: int, peer_node_type: int, peer_address: str):
        """Constructor."""
        self.peer_node_id = peer_node_id
        self.peer_node_type = peer_node_type
        self.peer_address = peer_address

        # (packed_request, req_num, local_data)
        self.pending_requests: Deque[Tuple[bytes, int, Any]] = collections.deque()

        self._conn_event: Union[ConnectionEvent, None] = None
        self._conn_event_write: Callable[[bytes], None] = self.not_connected
        self.connection_count: int = 0  # number of successful connections this peer has had (1 means no reconnects)

        self._free_req_num: int = 1  # req_num 0 is reserved for protocols sent without response

    @property
    def conn_event(self) -> Union[ConnectionEvent, None]:
        """Returns ConnectionEvent object associated with this ConnectionState."""
        return self._conn_event

    @property
    def is_connected(self) -> bool:
        """Returns True if this ConnectionState has an assigned ConnectionEvent."""
        return self._conn_event is not None

    @staticmethod
    def not_connected(packed_data: bytes) -> None:
        raise NoConnectionError

    def get_req_num(self) -> int:
        """Return a new request number."""
        new_req_num = self._free_req_num
        self._free_req_num += 1
        return new_req_num

    def assign_event(self, conn_event: ConnectionEvent) -> None:
        """Assigns the ConnectionEvent to this ConnectionState."""
        self._conn_event_write = conn_event.write_data
        self._conn_event = conn_event
        self.connection_count += 1

    def unassign_event(self) -> None:
        """Unassigns the current ConnectionEvent assigned."""
        self._conn_event_write = self.not_connected
        self._conn_event = None

    def write_data(self, packed_data: bytes) -> None:
        """Write packed data to out buffer for sending using the assigned ConnectionEvent."""
        self._conn_event_write(packed_data)


class NodeBase:
    """Node base class."""

    __slots__ = ('logger', 'node_name', 'node_id', 'node_type', 'interrupted', '_poll_events',
                 '_poll', '_poll_unblock_event')

    def __init__(self, system_config: Mapping, node_type: int):
        """Constructor."""
        self.node_name: str = system_config['general']['node_name']
        self.node_id: int = NODE_ID_UNASSIGNED
        self.node_type: int = node_type
        self.interrupted = False

        root_logger = logging.getLogger("emews_node")
        root_logger.setLevel(logging.DEBUG)
        root_logger.propagate = False  # don't propagate messages up to (logging) root

        log_config = system_config['logging']
        if system_config['debug']['node_local_logging']:
            # log local node output to a stream
            stream_path, stream_name = log_config['log_stream'].rsplit(".", 1)
            local_log_handler = logging.StreamHandler(
                stream=getattr(sys.modules[stream_path], stream_name))
            local_log_handler.setLevel(logging.DEBUG)  # local logging is for debugging
            local_log_handler.setFormatter(ConsoleFormatter(log_config['log_message_format_local']))
        else:
            # do not log local node output
            local_log_handler = logging.NullHandler()

        root_logger.addHandler(local_log_handler)

        self.logger = root_logger

        self.logger.info("eMews version %s", __version__)
        self.logger.info("Node name: %s, node type: %s", self.node_name, NAME_STR_NODE_TYPE[self.node_type])
        self.logger.info("Current working directory: %s", os.getcwd())

        self._poll_events: Dict[int, PollEvent] = {}  # [event_fd]-->Event
        self._poll = select.poll()

        self._poll_unblock_event = self._add_counter(self._handle_poll_unblock)

    def start(self) -> None:
        """Start the node."""
        raise NotImplementedError

    def stop(self) -> None:
        """Handle shutdown tasks pre event-loop stop."""
        if self.interrupted:
            return

        self.interrupted = True
        self._poll_unblock_event.increment()  # stop the polling loop

    def shutdown(self) -> None:
        """Handle shutdown tasks post event-loop stop."""
        pass

    def run(self) -> None:
        """Start the node, run the polling loop."""
        signal.signal(signal.SIGHUP, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)

        self.start()

        while not self.interrupted:
            poll_events = self._poll.poll()

            if self.interrupted:
                break

            for event_fd, event_flag in poll_events:
                event_obj = self._poll_events[event_fd]

                try:
                    event_obj.process(event_flag)
                except PollEventError as ex:
                    fileno = event_obj.fileno()
                    self._poll.unregister(fileno)
                    del self._poll_events[fileno]
                    self.logger.debug("Event with fd %d and type '%s' closed unexpectedly (%s)",
                                      fileno, type(event_obj).__name__, ex)
                    event_obj.close_unexpected(str(ex))

        self.logger.debug("Event polling loop stopped.  Invoking node shutdown ...")

        self.shutdown()

        self.logger.debug("Closing poll events ...")
        # close all events
        # This is performed last (after node shutdown) so any operations directly on poll events
        # will not fail due to the event being closed.
        for event_fileno, event_obj in self._poll_events.items():
            self._poll.unregister(event_fileno)
            event_obj.close()
            self.logger.debug("Event with fd %d and type '%s' closed due to node shutting down",
                              event_fileno, type(event_obj).__name__)

        self._poll_events.clear()

    def _send_net_request(self, conn_state: ConnectionState, protocol_id: int,
                          request_data: Sequence = (), local_data: Any = None) -> None:
        """Send a network request to peer."""
        protocol_obj = NET_PROTOCOL[protocol_id]

        new_req_num = conn_state.get_req_num()
        packed_data = protocol_obj.pack_request(new_req_num, request_data)
        conn_state.pending_requests.append((packed_data, new_req_num, local_data))

        self.logger.debug("New network request: peer node id: %d, protocol id: %d (req num=%d, pending queue=%d)",
                          conn_state.peer_node_id, protocol_id, new_req_num, len(conn_state.pending_requests))

        try:
            conn_state.write_data(packed_data)
        except NoConnectionError:
            self.logger.debug("No connection to node %d at %s, caching network request (protocol id: %d)",
                              conn_state.peer_node_id, conn_state.peer_address, protocol_id)

    def _send_net_request_nr(self, conn_state: ConnectionState, protocol_id: int, request_data: Sequence = ()) -> None:
        """Send a network request to peer without response.  These requests will not be cached."""
        protocol_obj = NET_PROTOCOL[protocol_id]

        packed_data = protocol_obj.pack_request(0, request_data)

        self.logger.debug("New network request: peer node id: %d, protocol id: %d (no queueing)",
                          conn_state.peer_node_id, protocol_id)

        try:
            conn_state.write_data(packed_data)
        except NoConnectionError:
            self.logger.debug("No connection to node %d at %s, dropping network request (protocol id: %d)",
                              conn_state.peer_node_id, conn_state.peer_address, protocol_id)

    def _event_register(self, event_obj: PollEvent, polling_mode: int) -> None:
        """Register new event."""
        fileno = event_obj.fileno()
        self._poll_events[fileno] = event_obj
        self._poll.register(fileno, polling_mode)

        self.logger.debug("New event registered with fd %d and type '%s'",
                          fileno, type(event_obj).__name__)

    def _event_close(self, event_obj: PollEvent) -> None:
        """Close the event."""
        fileno = event_obj.fileno()
        self._poll.unregister(fileno)
        del self._poll_events[fileno]
        event_obj.close()

        self.logger.debug("Event with fd %d and type '%s' closed by request", fileno, type(event_obj).__name__)

    def _add_counter(self, on_event: CounterEventCB) -> CounterEvent:
        """Add a new counter event (event_fd)."""
        new_counter = CounterEvent(on_event)
        self._event_register(new_counter, PollEvent.POLL_RO)
        return new_counter

    def _add_timer(self, on_timer_expiry: TimerEventCB) -> TimerEvent:
        """Add a new timer event (timer_fd)."""
        new_timer = TimerEvent(on_timer_expiry)
        self._event_register(new_timer, PollEvent.POLL_RO)
        return new_timer

    def _add_listener(self, port: int, on_connected_inbound: InboundConnectedCB) -> bool:
        """
        Create listener event for incoming connection attempts.
        Returns True if listener created, False otherwise.
        """
        if port < 1 or port > 65535:
            raise ValueError(f"Port out of range (must be between 1 and 65535), given: {port}")
        if port < 1024:
            self.logger.warning("Port is less than 1024 (given: %d).  Elevated permissions may be "
                                "needed for socket binding", port)

        try:
            sock_event = ListenerEvent(port, self._on_listener_accept, on_connected_inbound)
        except OSError as ex:
            self.logger.error("Could not create listener (port %d): %s", port, ex)
            self.stop()
            return False

        self._event_register(sock_event, PollEvent.POLL_RO)
        self.logger.info("Listening for incoming connections on port %d", port)
        return True

    def _add_outbound_connecting(self, port: int, conn_state: ConnectionState,
                                 on_connect_failed: ConnectFailedCB,
                                 on_outbound_connected: OutboundConnectedCB) -> None:
        """Initiate an outbound connection attempt to peer provided by conn_state."""
        conn_event = OutboundEvent(self.node_name, self.node_type, conn_state.connection_count, conn_state.peer_address,
                                   port, on_connect_failed, on_outbound_connected, self._on_polling_mode_update)
        self._event_register(conn_event, conn_event.polling_mode)

    def _add_connection(self, connecting_event: Union[InboundEvent, OutboundEvent],
                        conn_state: ConnectionState, on_disconnection: DisconnectionCB,
                        event_class=ConnectionEvent) -> None:
        """Create connection event for a connected socket (transfer from connecting event)."""
        assert connecting_event.peer_addr == conn_state.peer_address
        fileno = connecting_event.fileno()

        conn_event = event_class(self.logger, connecting_event.sock, conn_state, on_disconnection,
                                 self._on_polling_mode_update)

        assert fileno == conn_event.fileno()
        self._poll_events[fileno] = conn_event
        self._poll.modify(fileno, conn_event.polling_mode)

        self.logger.debug("Socket with fd %d transferred from connecting to connected", fileno)

    # callback methods
    def _on_polling_mode_update(self, event_obj: PollEvent, polling_mode: int) -> None:
        """Update polling mode of the event."""
        fileno = event_obj.fileno()
        self._poll.modify(fileno, polling_mode)
        self.logger.debug("Event with fd %d and type '%s' updated polling mode to %d",
                          fileno, type(event_obj).__name__, polling_mode)

    def _on_listener_accept(self, acc_sock: socket.socket, src_addr: str,
                            on_connected_inbound: InboundConnectedCB) -> None:
        """Handle an inbound connection."""
        conn_event = InboundEvent(acc_sock, src_addr, self._on_disconnected_inbound,
                                  on_connected_inbound, self._on_polling_mode_update)
        self._event_register(conn_event, conn_event.polling_mode)

    def _on_disconnected_inbound(self, src_addr: str, reason: str) -> None:
        """Handle disconnection on pending inbound connection."""
        self.logger.debug("Inbound connection with %s disconnected: %s", src_addr, reason)

    # event handlers
    def _handle_poll_unblock(self, event_obj, data):
        """Poll was manually unblocked."""
        # increment_counter() invoked on shutdown, this method should not be invoked
        self.logger.warning("Polling loop unblocked while not interrupted (fd: %d, counter: %d)",
                            event_obj.fileno(), data)

    # noinspection PyUnusedLocal
    def _shutdown_signal_handler(self, signum: int, frame):
        """Signal handler for incoming signals (those which are registered)."""
        if self.interrupted:
            return

        self.logger.info("Received local signum %d, shutting down node ...", signum)
        self.stop()


def node_init(args):
    """Node initialization."""
    config_dict = parse_system_config(node_config_path=args.node_config)

    # node name
    if args.node_name is not None:
        node_name = args.node_name
    else:
        node_name = config_dict['general']['node_name']
        if node_name is None:
            # node name is not defined anywhere, default to using node host name
            node_name = socket.gethostname()

    config_dict['general']['node_name'] = node_name

    if args.node_type == 'host':
        if args.hub_address is not None:
            config_dict['hub']['address'] = args.hub_address
        if args.hub_port is not None:
            config_dict['communication']['port'] = args.hub_port

        node_obj = getattr(importlib.import_module('emews.base.host'), 'HostNode')(config_dict)
    elif args.node_type == 'servspawn':
        config_dict['general']['node_name'] = f"{node_name}-servspawn"

        node_obj = getattr(importlib.import_module('emews.base.hostproc'), 'ServiceSpawner')(
            config_dict, args.service_name, args.service_configuration)
    elif args.node_type == 'monitor':
        if args.hub_address is not None:
            config_dict['hub']['address'] = args.hub_address
        if args.hub_port is not None:
            config_dict['communication']['port'] = args.hub_port
        if not args.log_local:
            # only log local if explicitly said to as cmd arg
            config_dict['debug']['node_local_logging'] = False

        config_dict['general']['node_start_delay'] = 0  # no need for a start delay

        node_obj = getattr(importlib.import_module('emews.base.hubproc'), 'HubMon')(config_dict)
    elif args.node_type == 'console':
        if args.hub_address is not None:
            config_dict['hub']['address'] = args.hub_address
        if args.hub_port is not None:
            config_dict['communication']['port'] = args.hub_port
        if not args.log_local:
            # only log local if explicitly said to as cmd arg
            config_dict['debug']['node_local_logging'] = False

        config_dict['general']['node_start_delay'] = 0  # no need for a start delay

        node_obj = getattr(importlib.import_module('emews.base.hubproc'), 'HubConsole')(config_dict)
    elif args.node_type == 'hub':
        if args.scn_autostart:
            # enable experiment scenario autostart
            config_dict['hub']['scenario_autostart'] = True
        node_obj = getattr(importlib.import_module('emews.base.hub'), 'HubNode')(config_dict)
    else:
        # this shouldn't happen as argparse catches invalid node types
        raise AttributeError(f"Invalid node type given: {args.node_type}")

    return node_obj
