"""Base module for eMews services."""
from typing import Any, Callable, Deque, Dict, List, Mapping, Set, Tuple, Type, Union

import collections
import importlib
import logging
import pickle
import struct
import traceback

from threading import Condition, Event, Lock, Thread
from time import perf_counter

from emews.base.config import parse_service_config, get_service_class_name
from emews.base.env_key import EnvironmentKey, ENV_KEY_TYPE
from emews.base.node import NetProtocolID


class ServiceInterrupted(Exception):
    """Raised when a service is interrupted and a service call is invoked or service blocked."""
    pass


class ServiceLoadError(Exception):
    """Raised when a service cannot be imported."""
    pass


class ServiceControlError(Exception):
    """Raised when a service command (start/stop/exit) fails."""
    pass


# noinspection PyUnusedLocal
def no_call_interrupted(*args, **kwargs):
    raise ServiceInterrupted


def load_service(service_name: str, config_filename: str) -> Tuple[Type['Service'], Dict]:
    """Import a service class and configuration."""
    try:
        service_config = parse_service_config(service_name, config_filename)
    except Exception as ex:
        # the parser is dependent on third party YAML parsers, catch all exceptions here and re-raise
        raise ServiceLoadError(f"Service configuration for service '{service_name}' could not be loaded: {ex}") from ex

    if 'parameters' not in service_config:
        raise ServiceLoadError(
            f"Service configuration for service '{service_name}' missing required section: 'parameters'")

    service_class_str = get_service_class_name(service_config)

    try:
        service_class = getattr(importlib.import_module(f"emews.services.{service_name}.service"),
                                service_class_str)
    except (AttributeError, ImportError, SyntaxError) as ex:
        raise ServiceLoadError(
            f"Service '{service_name}' (service class: {service_class_str}) could not be loaded: {ex}") from ex

    return service_class, service_config


class Service:
    """Service base class."""

    __slots__ = ('_logger', '_cb_service_call',)

    def __init_subclass__(cls, **kwargs):
        """Subclass creation hook.  'cls' is the subclass (child Service)."""
        super().__init_subclass__(**kwargs)
        service_init = cls.__init__  # subclass init will have a different signature (config arg)

        def __init__(self: Service, config: Mapping, *init_args, **init_kwargs):
            """Child service __init__ override."""
            if not hasattr(self, '_logger'):
                # this will be true only for the concrete child class (last one in inheritance chain)
                assert len(init_args) == 2 and not len(init_kwargs)
                self._logger = init_args[0]  # unique logger to service instance
                self._cb_service_call = init_args[1]

                service_init(self, config)
                return

            # config is required, anything else is optional, passed by child in super().__init__()
            service_init(self, config, *init_args, **init_kwargs)

        setattr(cls, '__init__', __init__)  # replace child class init with the def above

    def service_run(self) -> None:
        """Point of entry for running the service."""
        raise NotImplementedError

    def service_exit(self) -> None:
        """Called when a service exits, either by interruption or service_run() exit.  Handle any cleanup here."""
        pass

    @property
    def logger(self) -> logging.Logger:
        """System logger."""
        return self._logger

    def interrupted(self) -> bool:
        """Return interrupted flag.  If True, service should quickly stop its execution."""
        return self._cb_service_call(ServiceImpl.CALL_INDEX_INTERRUPTED)

    def elapsed_time(self) -> float:
        """Return the elapsed time from start of service run."""
        return self._cb_service_call(ServiceImpl.CALL_INDEX_ELAPSED_TIME)

    def sleep(self, duration: Union[float, int]) -> None:
        """Suspend execution of service for the given amount of time (in seconds)."""
        if duration < 0 or duration is None:
            duration = 0
        self._cb_service_call(ServiceImpl.CALL_INDEX_SLEEP, duration)

    def send_all(self, data: Any) -> None:
        """Send data to all running services that are designated as receivers."""
        self._cb_service_call(ServiceImpl.CALL_INDEX_SEND_ALL, data)

    def send_to(self, data: Any, *to_service_ids: int) -> None:
        """Send data to all running services in to_service_ids that are designated as receivers."""
        self._cb_service_call(ServiceImpl.CALL_INDEX_SEND_TO, to_service_ids, data)

    def recv(self) -> Tuple[int, Any]:
        """Wait until data is received through the Hub.  Returns the service id which sent the data, and the data."""
        return self._cb_service_call(ServiceImpl.CALL_INDEX_RECV_MSG)

    def received_data(self) -> bool:
        """Returns True if there is data waiting to be fetched using recv()."""
        return self._cb_service_call(ServiceImpl.CALL_INDEX_HAS_RECV)

    def tell(self, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Give an observation to the network environment."""
        self._cb_service_call(ServiceImpl.CALL_INDEX_TELL, obs_key, obs_val)

    def ask(self, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Ask evidence from the network environment."""
        return self._cb_service_call(ServiceImpl.CALL_INDEX_ASK, ev_key)


class ServiceImpl:
    """Service implementation."""

    CALL_INDEX_INTERRUPTED = 0
    CALL_INDEX_SLEEP = 1
    CALL_INDEX_SEND_ALL = 2
    CALL_INDEX_SEND_TO = 3
    CALL_INDEX_RECV_MSG = 4
    CALL_INDEX_HAS_RECV = 5
    CALL_INDEX_TELL = 6
    CALL_INDEX_ASK = 7
    CALL_INDEX_ELAPSED_TIME = 8

    __slots__ = ('logger_dist', 'service_id', 'service_thread', '_thread_event', '_start_time', '_is_running',
                 '_do_exit', '_service_calls', '_interrupted', '_events', '_event_set_lock', '_cv',
                 '_recv_queue', '_cb_service_exit', '_cb_send_net_request', '_cb_get_key_id')

    def __init__(self, dist_logger: logging.Logger, service_id: int, service_full_name: str,
                 thread_args: Tuple[logging.Logger, Type[Service], Mapping, Callable[..., None], Callable[..., None]],
                 cb_get_key_id: Callable[[EnvironmentKey], int],
                 cb_send_net_request: Callable[..., None]):
        """Constructor."""
        self.logger_dist = dist_logger  # node distributed logger

        self.service_id = service_id  # service instance id
        self._cb_send_net_request = cb_send_net_request
        self._cb_get_key_id = cb_get_key_id

        self._service_calls = self._init_call_list()

        self._start_time = 0.0  # start timestamp of current run

        self._events: Set[Event] = set()  # set of current events (from any service call in any service thread)
        self._event_set_lock = Lock()  # thread safe access to self._events

        self._thread_event = Event()  # event controlling blocks in the main thread method

        self._is_running = False  # True when service is running (service_run() is invoked)
        self._do_exit = False  # True when service thread is asked to terminate

        self._cv = Condition()
        self._recv_queue: Deque[Tuple[int, bytes]] = collections.deque()  # incoming data from other services

        self._interrupted = False

        self.service_thread = Thread(
            target=self._thread_entry,
            args=thread_args,
            name=service_full_name,
            daemon=True)

    @property
    def name(self) -> str:
        """Returns the full service name."""
        return self.service_thread.name

    # start/stop/exit methods are called from the main thread
    def start(self) -> None:
        """Invoke the service_run() method.  Service must have instantiated (thread is active)."""
        if not self.is_active():
            raise ServiceControlError("service thread is not active")

        if self._do_exit:
            raise ServiceControlError("service thread is requested to terminate")

        if self._thread_event.is_set():
            raise ServiceControlError("service was already requested to start")

        if self._is_running:
            raise ServiceControlError("service is already running")

        self._thread_event.set()  # unblock service thread

    def stop(self) -> None:
        """Interrupt the service."""
        if not self.is_active():
            raise ServiceControlError("service thread is not active")

        if self._do_exit:
            raise ServiceControlError("service thread is requested to terminate")

        if self._interrupted:
            raise ServiceControlError("service was already requested to stop")

        if not self._is_running:
            raise ServiceControlError("service is already stopped")

        self._interrupt_service()

    def exit(self) -> None:
        """Shuts down the service thread."""
        if not self.is_active():
            raise ServiceControlError("service thread is not active")

        if self._do_exit:
            raise ServiceControlError("service thread was already requested to terminate")

        self._do_exit = True
        self._interrupt_service()
        self._thread_event.set()

    def is_active(self) -> bool:
        """Return if service thread is active (thread is running)."""
        return self.service_thread.is_alive()

    def is_running(self) -> bool:
        """Return if service is running (service_run() method invoked)"""
        return self._is_running

    def is_interrupted(self) -> bool:
        """Return if the service has been requested to stop."""
        return self._interrupted

    def _thread_entry(self, service_logger: logging.Logger, service_cls, service_config: Mapping,
                      cb_service_init: Callable[..., None],
                      cb_service_exit: Callable[..., None]):
        """Point of entry for a thread of execution."""
        try:
            service_instance: Service = service_cls(service_config['parameters'], service_logger,
                                                    lambda call_index, *args: self._service_calls[call_index](*args))
        except Exception as ex:
            # need to catch everything here - exception occurred in service init
            self.logger_dist.error("Instantiation failed due to exception: %s", ex)
            self._do_exit = True
            cb_service_init(self, ex, traceback.format_exc())
            return

        # instantiation successful
        cb_service_init(self)
        self.logger_dist.info("Instantiated")

        while not self._do_exit:
            self._thread_event.wait()

            if self._do_exit:
                break

            assert not len(self._events)

            self._service_calls = self._init_call_list()

            self._cb_send_net_request(NetProtocolID.HUB_SERVICE_STARTED, request_data=(self.service_id,))
            self.logger_dist.info("Started")

            # Order here is important for thread safety on start().  start() checks for event.is_set() first, so by
            # clearing the set flag second, we are guaranteed that is_running = True by the time a caller to start()
            # could get past the is_set() condition.
            self._is_running = True
            self._thread_event.clear()

            self._start_time = perf_counter()

            try:
                service_instance.service_run()
            except ServiceInterrupted:
                service_instance.service_exit()  # allow service to handle any cleanup tasks
            except Exception as ex:
                # need to catch everything here - exception occurred in service
                self.logger_dist.error("Terminating due to exception: %s", ex)

                self._do_exit = True
                # A start/stop/exit call could slip through, resulting in any of thread event being set and
                # service_interrupt() being called, both outcomes of which do not affect thread shutdown.
                self._is_running = False
                cb_service_exit(self, ex, traceback.format_exc())
                return

            self._cb_send_net_request(NetProtocolID.HUB_SERVICE_STOPPED, request_data=(self.service_id,))
            self.logger_dist.info("Stopped")

            # ordering here is important for thread safety of stop()
            self._is_running = False  # any start() call before we get to the wait is fine; wait() will return
            self._interrupted = False

        cb_service_exit(self)
        self.logger_dist.info("Exited")
        return

    def _init_call_list(self) -> List[Callable]:
        """Initialize the call list for a service run."""
        return [self._sc_interrupted,
                self._sc_sleep,
                self._sc_send_all,
                self._sc_send_to,
                self._sc_recv,
                self._sc_has_recv,
                self._sc_tell,
                self._sc_ask,
                self._sc_elapsed_time]

    def _interrupt_service(self) -> None:
        """Interrupt the service."""
        if self._interrupted:
            return

        self._interrupted = True

        # Replace all service calls except first with exception throw function.
        # First service call is to check for interrupted, so leave that one.
        # Service call replacement enables most service calls to not have to check for interrupted.
        self._service_calls[1:] = [no_call_interrupted] * (len(self._service_calls) - 1)

        with self._event_set_lock:
            for service_event in self._events:
                service_event.set()

        with self._cv:
            self._cv.notify_all()  # notify all threads associated with this service

    def _new_event(self) -> Event:
        """Create new Event instance."""
        new_event = Event()
        with self._event_set_lock:
            if self._interrupted:
                # set flag on this event so wait() will not block; do not add to set
                new_event.set()
                return new_event

            self._events.add(new_event)

        return new_event

    def _del_event(self, event: Event) -> None:
        """Remove the given Event."""
        with self._event_set_lock:
            # because these events are not reused, we don't need to clear() them
            self._events.remove(event)

    def recv_data(self, from_service_id: int, data: bytes) -> None:
        """Receive data from a peer, given by from_service_id.  Services can receive data even when not running."""
        with self._cv:
            self._recv_queue.append((from_service_id, data))
            self._cv.notify()  # service may or may not be blocked

    # service callbacks (service thread execution)
    def _sc_interrupted(self) -> bool:
        """Return interrupted flag."""
        return self._interrupted

    def _sc_elapsed_time(self) -> float:
        """Return the elapsed time from start of service run."""
        return perf_counter() - self._start_time

    def _sc_sleep(self, duration: Union[float, int]) -> None:
        """Suspend execution of service for the given amount of time (in seconds)."""
        self.logger_dist.debug("Sleeping for %.2f seconds ...", duration)
        service_event = self._new_event()
        service_event.wait(timeout=duration)
        self._del_event(service_event)

    def _sc_send_all(self, data: Any) -> None:
        """Send data to all services based on service class matching."""
        service_event = self._new_event()

        self._cb_send_net_request(NetProtocolID.HUB_SERVICE_SEND_ALL,
                                  request_data=(self.service_id, pickle.dumps(data)),
                                  local_data=service_event)
        service_event.wait()

        self._del_event(service_event)

    def _sc_send_to(self, to_service_ids: Tuple[int, ...], data: Any) -> None:
        """Send data to all services in list based on service class matching."""
        service_event = self._new_event()

        self._cb_send_net_request(NetProtocolID.HUB_SERVICE_SEND_TO,
                                  request_data=(self.service_id, pickle.dumps(to_service_ids), pickle.dumps(data)),
                                  local_data=service_event)

        service_event.wait()

        self._del_event(service_event)

    def _sc_has_recv(self) -> bool:
        """Returns True if recv queue is non-empty."""
        return len(self._recv_queue) > 0

    def _sc_recv(self) -> Tuple[int, Any]:
        """Wait until data is received through the Hub."""
        with self._cv:
            if self._interrupted:
                # It's possible that this method is entered on interrupt() but before the service call list is updated,
                # and the interrupt() method grabs the lock first.  In that case, when we enter here, without this
                # check, we may get stuck in a wait(), as notify_all() would have been called before we entered.
                # With the GIL, this wouldn't happen, but better to cover our bases.
                raise ServiceInterrupted

            while not len(self._recv_queue):
                # If a message is waiting already, simply return it, otherwise it is possible that
                # wait() may return without actually being notified, so check queue again...
                # A wait() call will release the lock, allowing another thread associated with this service to enter.
                # This may cause another wait(), or if the thread enters after service_recv_data() is called (it gets
                # the lock, then another service thread), it may grab the data, resulting in a notified thread staying
                # in the loop.  While the ordering may be indeterministic, this is thread safe for multiple service
                # threads to call.
                self._cv.wait()

                if self._interrupted:
                    # wait() call may have returned due to service interrupt request
                    raise ServiceInterrupted

            self.logger_dist.debug("Retrieving message (messages remaining in queue: %d)", len(self._recv_queue) - 1)
            from_service_id, data = self._recv_queue.popleft()
            return from_service_id, pickle.loads(data)

    def _sc_tell(self, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Give an observation to the network environment."""
        obs_key_id = self._cb_get_key_id(obs_key)

        s_obs = struct.pack(f">L{obs_key.key_list_type * len(obs_val)}", len(obs_val), *obs_val)

        service_event = self._new_event()

        self._cb_send_net_request(NetProtocolID.HUB_SERVICE_TELL,
                                  request_data=(self.service_id, obs_key_id, s_obs,),
                                  local_data=service_event)

        service_event.wait()

        self._del_event(service_event)

    def _sc_ask(self, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Ask evidence from the network environment."""
        ev_key_id = self._cb_get_key_id(ev_key)

        ev_lst = []  # list to write evidence values to

        service_event = self._new_event()

        self._cb_send_net_request(NetProtocolID.HUB_SERVICE_ASK,
                                  request_data=(self.service_id, ev_key_id),
                                  local_data=(service_event, ev_key, ev_lst))
        service_event.wait()

        self._del_event(service_event)

        if self._interrupted:
            # wait() call may have returned due to service interrupt request
            raise ServiceInterrupted

        return tuple(ev_lst)
