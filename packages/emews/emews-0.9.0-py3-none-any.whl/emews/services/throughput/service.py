"""
Throughput stats.

Outputs as log messages to the hub send/recv throughput for all interfaces on the node this service
is running on.  Currently IPv4 only.
"""
import socket

import psutil

from emews.api.service import Service


class DefaultService(Service):
    """Classdocs."""

    __slots__ = ('_if_info', '_output_interval', '_tr_unit', '_tr_scale')

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        interface_prefixes = config['interface_prefixes']  # list

        output_interval = config['output_interval']
        if output_interval < 1:
            raise AttributeError("Output interval must be 1 or greater.")

        self._output_interval = output_interval

        tr_unit = config['output_unit']

        if tr_unit == 'k':
            # scale to get appropriate unit and per second
            # Kbps
            self._tr_scale = self._output_interval * 0.0078125  # 8/1024
        elif tr_unit == 'm':
            # mbps
            self._tr_scale = self._output_interval * 0.00000762939453125  # 8/(1024*1024)
        else:
            raise AttributeError(f"Output unit '{tr_unit}' invalid.")

        self._tr_unit = tr_unit
        self._if_info = {}  # stores current interface info

        ifs = psutil.net_if_addrs()
        for if_name, if_addrs in ifs.items():
            for prefix in interface_prefixes:
                if not if_name.startswith(prefix):
                    continue

                # interface is in our prefix list
                self._if_info[if_name] = {}
                # create addr string
                ipv4_str = "0.0.0.0"
                for if_addr in if_addrs:
                    # store the first IPv4 address we find, or the default if none can be found
                    if if_addr.family == socket.AF_INET:
                        ipv4_str = if_addr.address
                        self.logger.info("Monitoring NIC: %s (IPv4 address: %s)", if_name, ipv4_str)
                        break

                self._if_info[if_name]['addr_str'] = ipv4_str
                # create other map keys
                self._if_info[if_name]['b_sent'] = 0  # number of sent bytes (total)
                self._if_info[if_name]['b_recv'] = 0  # number of received bytes (total)

    def service_run(self):
        """Output throughput on all interfaces every 'output_interval' seconds."""
        # initialize the S/R byte counts to what they are currently to calibrate
        net_stats = psutil.net_io_counters(pernic=True)
        for if_name, if_info in self._if_info.items():
            if_info['b_sent'] = net_stats[if_name].bytes_sent
            if_info['b_recv'] = net_stats[if_name].bytes_recv

        self.sleep(self._output_interval)

        while not self.interrupted():
            msg_str = ""
            net_stats = psutil.net_io_counters(pernic=True)

            for if_name, if_info in self._if_info.items():
                bytes_sent = net_stats[if_name].bytes_sent
                bytes_recv = net_stats[if_name].bytes_recv

                # throughput in kbps
                tr_sent = (bytes_sent - if_info['b_sent']) * self._tr_scale
                tr_recv = (bytes_recv - if_info['b_recv']) * self._tr_scale
                msg_str = f"{msg_str}{if_info['addr_str']}: [S: {tr_sent:.2f} {self._tr_unit}bps, "\
                          f"R: {tr_recv:.2f} {self._tr_unit}bps] "
                # update the total bytes sent/recv
                if_info['b_sent'] = bytes_sent
                if_info['b_recv'] = bytes_recv

            self.logger.info(msg_str)

            # note that this is not entirely accurate, as the logic itself adds to the interval
            self.sleep(self._output_interval)
