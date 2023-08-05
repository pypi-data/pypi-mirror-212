"""Automates the process of a user interacting with an SSH client."""
from typing import List

from pexpect import pxssh

from emews.api.random import TruncnormInt, UniformInt
from emews.api.service import Service


class DefaultService(Service):
    """Classdocs."""

    __slots__ = ('_ssh_session', '_host', '_port', '_username', '_password', '_command_list',
                 '_num_commands_sampler', '_command_sampler_sigma', '_command_delay_sampler',
                 '_crawl_sampler')

    def __init__(self, config: dict):
        """Constructor."""
        super().__init__()

        self._host = config['host']
        self._port = config['port']
        self._username = config['username']
        self._password = config['password']

        self._command_list: List[str] = config['command_list']

        self._num_commands_sampler = TruncnormInt(**config['num_commands_sampler'])
        self._command_delay_sampler = UniformInt(**config['command_delay_sampler'])
        self._crawl_sampler = UniformInt(**config['crawl_sampler'])

        self._command_sampler_sigma = config['command_sampler']['sigma']

        self._ssh_session = None

    def service_run(self):
        """Connect and login to the ssh server given with the credentials given."""
        self.logger.debug("Distributions: num_commands: %s, command_delay: %s, crawl: %s, "
                          "command: sigma=%s (upper_bound set dynamically)",
                          str(self._num_commands_sampler), str(self._command_delay_sampler),
                          str(self._command_delay_sampler), str(self._command_sampler_sigma))

        while not self.interrupted():
            self.sleep(self._crawl_sampler.sample())
            self._ssh_crawl()

    def service_exit(self) -> None:
        """Close the connection upon service interrupted while blocked."""
        ssh_client = self._ssh_session
        if ssh_client is not None:
            ssh_client.close()

    def _ssh_crawl(self):
        """
        Perform a single login and SSH crawl.

        Note, if using CORE, a new key-pair is generated for each network session.  This can result in SSH connections
        failing after one session, due to a new key-pair which doesn't match with what is in /root/.ssh/known_hosts.
        Assuming CORE is being run on a dedicated system, delete the known_hosts file before every CORE session.
        """
        ssh_client = pxssh.pxssh()
        self._ssh_session = ssh_client

        self.logger.info("Connecting to SSH server at %s:%d, user='%s' ...",
                         self._host, self._port, self._username)

        ssh_client.force_password = True
        ssh_client.login(self._host,
                         self._username,
                         password=self._password,
                         port=self._port)

        self.logger.info("Connected to SSH server (%s@%s:%d), executing commands ...", self._username, self._host,
                         self._port)

        # As we are sampling without replacement, we need to copy the original list
        command_list = list(self._command_list)
        cmd_sigma = self._command_sampler_sigma

        executed_commands: List[str] = []

        # loop until command count reached
        num_commands = self._num_commands_sampler.sample()
        for _ in range(num_commands):
            command_sampler = TruncnormInt(upper_bound=len(command_list) - 1, sigma=cmd_sigma)
            next_command = command_list.pop(command_sampler.sample())

            executed_commands.append(next_command)

            ssh_client.sendline(next_command)
            ssh_client.prompt()

            self.sleep(self._command_delay_sampler.sample())

        self.logger.info("Commands executed: [%s]", ", ".join(executed_commands))
        self.logger.info("Logging out (%s@%s:%d) ...", self._username, self._host, self._port)

        ssh_client.logout()
        ssh_client.close()
        self._ssh_session = None
