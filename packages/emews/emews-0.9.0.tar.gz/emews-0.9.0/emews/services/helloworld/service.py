"""Example service.  Logs 'Hello world!' periodically."""

from emews.api.service import Service
from emews.environments.example.keys import Evidence


class DefaultService(Service):
    """Default service class."""

    __slots__ = ('_log_interval', '_use_env')

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        self._log_interval = config['log_interval']
        self._use_env = config['use_env']

    def service_run(self):
        """Run the service."""
        self.logger.info("Hello world using an output interval of %d seconds (use environment: %s)",
                         self._log_interval, self._use_env)

        if self._use_env:
            # use example environment
            while not self.interrupted():
                # Note, the amount of time it takes to get the evidence will not be factored into
                # the sleep time, resulting in a longer interval than specified.
                global_req_count = self.ask(Evidence.HELLO_WORLD)[0]
                self.logger.info("Hello world! (global environment request count: %d)",
                                 global_req_count)
                self.sleep(self._log_interval)
        else:
            while not self.interrupted():
                self.logger.info("Hello world!")
                self.sleep(self._log_interval)


class DistWorldServer(Service):
    """Distributed hello world server."""

    __slots__ = ()

    def __init__(self, config):
        """Constructor."""
        super().__init__()

    def service_run(self):
        """Run the service."""
        self.logger.info("Listening for message ...")
        while not self.interrupted():
            # recv() blocks, unblocking on received data or if service is interrupted.  In the latter,
            # service_cleanup() will be called so the service can handle any cleanup
            sender_service_id, msg = self.recv()
            self.logger.info("Received message from service id %d: %s", sender_service_id, msg)


class DistWorldClient(Service):
    """Distributed hello world client."""

    __slots__ = ('_send_interval',)

    def __init__(self, config):
        """Constructor."""
        super().__init__()

        self._send_interval = config['send_interval']

    def service_run(self):
        """Run the service."""
        self.logger.info("Distributed hello world using a message send interval of %d seconds",
                         self._send_interval)

        while not self.interrupted():
            self.send_all("Hello world!")
            self.sleep(self._send_interval)
