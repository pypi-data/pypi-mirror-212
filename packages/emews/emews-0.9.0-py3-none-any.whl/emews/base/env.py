"""Base module for eMews environments."""
from typing import Callable, Dict, List, Set, Tuple, Type

import importlib
import inspect
import logging
import os
import struct

from emews.base.config import get_environments_path
from emews.base.env_key import ENV_KEY_TYPE, EnvironmentKey
from emews.base.node import NetworkHandlerError, TimerEvent, EventCloseCB, TYPE_LEN


TYPE_LEN_INT = TYPE_LEN['L']


class NetEnvError(Exception):
    """Raised when a network environment or the manager encounters an issue."""
    pass


class Environment:
    """Network environment base class."""

    __slots__ = ('_logger', '_cb_env_call')

    def __init_subclass__(cls, **kwargs):
        """Subclass creation hook.  'cls' is the subclass (child Environment)."""
        super().__init_subclass__(**kwargs)
        child_init = cls.__init__

        def __init__(self: Environment, logger_dist: logging.Logger, cb_sys: Callable):
            """Child service __init__ override."""
            self._logger = logger_dist
            self._cb_env_call = cb_sys

            child_init(self)

        setattr(cls, '__init__', __init__)  # replace child class init with the def above

    @property
    def logger(self) -> logging.Logger:
        """System logger."""
        return self._logger

    def update_evidence(self, node_id: int, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Produce evidence, given the observation."""
        raise NotImplementedError

    def get_evidence(self, node_id: int, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Return current evidence corresponding to the evidence key."""
        raise NotImplementedError

    def tell_to(self, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Give an observation to an environment."""
        self._cb_env_call(EnvState.CALL_INDEX_TELL_TO, obs_key, obs_val)

    def ask_from(self, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Ask for evidence from an environment."""
        return self._cb_env_call(EnvState.CALL_INDEX_ASK_FROM, ev_key)

    def new_timer(self, interval: int, callback_func: Callable, repeat=True) -> int:
        """
        Create a new timer, in which callback_func is invoked every 'interval' seconds, unless repeat=False.

        Return a unique identifier for the timer.
        """
        return self._cb_env_call(EnvState.CALL_INDEX_NEW_TIMER, interval, callback_func, repeat=repeat)

    def del_timer(self, timer_id: int) -> None:
        """Remove the timer with identifier 'timer_id'."""
        self._cb_env_call(EnvState.CALL_INDEX_DEL_TIMER, timer_id)


class EnvState:
    """Environment state."""

    CALL_INDEX_TELL_TO = 0
    CALL_INDEX_ASK_FROM = 1
    CALL_INDEX_NEW_TIMER = 2
    CALL_INDEX_DEL_TIMER = 3

    __slots__ = ('logger_dist', 'keys_obs', 'keys_ev', 'env_update_evidence', 'env_get_evidence',
                 '_call_list', '_timer_events', '_timer_cb', '_cb_env_tell_to', '_cb_env_ask_from',
                 '_cb_env_timer', '_cb_event_close', 'module_name', '_env')

    def __init__(self, logger_dist: logging.Logger, module_name: str, env_cls: Type[Environment],
                 cb_env_tell_to: Callable, cb_env_ask_from: Callable, cb_env_timer: Callable,
                 cb_event_close: EventCloseCB):
        """Constructor."""
        self._call_list = [self._ec_tell_to,
                           self._ec_ask_from,
                           self._ec_new_timer,
                           self._ec_del_timer]

        self._timer_events: Dict[int, TimerEvent] = {}
        self._timer_cb: Dict[TimerEvent, Callable] = {}

        # env manager callbacks
        self._cb_env_tell_to = cb_env_tell_to
        self._cb_env_ask_from = cb_env_ask_from
        self._cb_env_timer = cb_env_timer
        self._cb_event_close = cb_event_close

        self.keys_obs: Set[EnvironmentKey] = set()
        self.keys_ev: Set[EnvironmentKey] = set()

        self.logger_dist = logger_dist
        self.module_name = module_name

        # ignore argument sig mismatch - args injected
        self._env = env_cls(self.logger_dist, lambda call_index, *args: self._call_list[call_index](*args))
        self.env_update_evidence = self._env.update_evidence
        self.env_get_evidence = self._env.get_evidence

    @property
    def full_name(self) -> str:
        return f"{self.module_name}.{self._env.__class__.__name__}"

    @property
    def obs_key_names(self) -> List[str]:
        """Return a listing of all observation environment keys by name."""
        return [obs_key.key_full_name() for obs_key in self.keys_obs]

    @property
    def ev_key_names(self) -> List[str]:
        """Return a listing of all evidence environment keys by name."""
        return [ev_key.key_full_name() for ev_key in self.keys_ev]

    def _handle_timer_expiry(self, timer_event: TimerEvent, num_expires: int):
        """Handle a timer expiry."""
        self._timer_cb[timer_event](timer_event.fileno(), num_expires)  # invoke env callback

    # environment callbacks
    def _ec_tell_to(self, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Give an observation to an environment."""
        self._cb_env_tell_to(self, obs_key, obs_val)

    def _ec_ask_from(self, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Ask for evidence from an environment."""
        return self._cb_env_ask_from(self, ev_key)

    def _ec_new_timer(self, interval: int, callback_func: Callable, repeat) -> int:
        """
        Create a new timer, in which callback_func is invoked every 'interval' seconds, unless repeat=False.

        Return a unique identifier for the timer.
        """
        timer_event: TimerEvent = self._cb_env_timer(interval, self._handle_timer_expiry, repeat=repeat)
        timer_fd = timer_event.fileno()

        self._timer_cb[timer_event] = callback_func
        self._timer_events[timer_fd] = timer_event

        return timer_fd

    def _ec_del_timer(self, timer_id: int) -> None:
        """Remove the timer with identifier 'timer_id'."""
        try:
            timer_event = self._timer_events[timer_id]
        except KeyError:
            raise NetEnvError(f"environment timer {timer_id} does not exist")

        del self._timer_events[timer_id]
        del self._timer_cb[timer_event]
        self._cb_event_close(timer_event)


class EnvManager:
    """Manager for network environments."""

    __slots__ = ('logger_dist', '_cb_new_timer', '_env_state',
                 '_cb_event_close', '_key_id_by_name', '_key_by_id', '_env_state_by_key')

    def __init__(self, logger_dist: logging.Logger,
                 new_timer_cb: Callable, event_close_cb: EventCloseCB):
        """Constructor."""
        self.logger_dist = logger_dist
        self._cb_new_timer = new_timer_cb
        self._cb_event_close = event_close_cb

        self._key_id_by_name: Dict[str, int] = {}  # key name to its id (member value)
        self._key_by_id: Dict[int, EnvironmentKey] = {}  # key id to its member (enum)
        self._env_state_by_key: Dict[EnvironmentKey, EnvState] = {}  # env key to its env
        self._env_state: Set[EnvState] = set()

    @property
    def env_count(self) -> int:
        """Return the number of environments."""
        return len(self._env_state)

    @property
    def env_names(self) -> List[str]:
        """Return a listing of all environments by name."""
        return [env_state.full_name for env_state in self._env_state]

    @property
    def env_key_names(self) -> List[str]:
        """Return a listing of all environment keys by name."""
        key_lst = [key_obs.key_full_name() for env_state in self._env_state
                   for key_obs in env_state.keys_obs]
        key_lst.extend([key_ev.key_full_name() for env_state in self._env_state
                        for key_ev in env_state.keys_ev])
        return key_lst

    def parse_environments(self, logger: logging.Logger) -> None:
        """Instantiate all environments found."""
        with os.scandir(get_environments_path()) as it_environment_root:
            for entry_env_root in it_environment_root:
                env_module_name = None
                env_cls_obj = None
                keys_module_obj = None
                keys_import_fail = False

                if not entry_env_root.name.startswith('.') and entry_env_root.is_dir():
                    # may be a environment directory
                    env_module_name = entry_env_root.name

                    with os.scandir(entry_env_root.path) as it_dir:
                        # check if contents are consistent with an environment
                        for entry_dir in it_dir:
                            if entry_dir.is_file() and entry_dir.name == 'environment.py':
                                try:
                                    env_module_obj = importlib.import_module(
                                        f"emews.environments.{env_module_name}.environment")
                                except ImportError as ex:
                                    # apparently not a module
                                    logger.warning(
                                        "While parsing environments: directory '%s' contains "
                                        "environment.py but cannot be imported: %s",
                                        env_module_name, ex)
                                    break

                                env_cls_lst = []
                                # Get environment classes (only should be one to preserve 1:1
                                # mapping from keys - which environment to use is based on the
                                # env key itself, ie, environments are looked up based on key)
                                for name, obj in inspect.getmembers(env_module_obj):
                                    if inspect.isclass(obj) and issubclass(obj, Environment) and \
                                            obj != Environment:
                                        # environment class (child of Environment)
                                        env_cls_lst.append(obj)

                                if not len(env_cls_lst):
                                    logger.warning("While parsing environments: directory '%s' contains "
                                                   "environment.py but missing an Environment class",
                                                   env_module_name)
                                    break

                                if len(env_cls_lst) > 1:
                                    logger.warning("While parsing environments: directory '%s' contains "
                                                   "environment.py but more than one Environment class.",
                                                   env_module_name)
                                    break

                                env_cls_obj = env_cls_lst[0]

                            elif entry_dir.is_file() and entry_dir.name == 'keys.py':
                                try:
                                    keys_module_obj = importlib.import_module(
                                        f"emews.environments.{env_module_name}.keys")
                                except ImportError as ex:
                                    # apparently not a module (or EnvironmentKey creation failed)
                                    logger.warning("While parsing environments: directory '%s' contains "
                                                   "keys.py but cannot be imported: %s", env_module_name, ex)
                                    keys_import_fail = True
                                    break

                # Note, a directory missing an environment module but has a keys module will be
                # ignored (no warnings logged).
                if env_cls_obj is None or keys_import_fail:
                    # environment module or class missing, or keys module failed to import (this
                    # latter condition is here to prevent two warnings to log in terms of keys)
                    continue

                if keys_module_obj is None:
                    logger.warning("While parsing environments: directory '%s' contains "
                                   "environment.py but missing a keys module", env_module_name)
                    continue

                env_state = EnvState(self.logger_dist, env_module_name, env_cls_obj,
                                     self._env_tell_to, self._env_ask_from, self._cb_new_timer,
                                     self._cb_event_close)
                self._env_state.add(env_state)

                # get env keys (obs/ev)
                for cls_name, obj in inspect.getmembers(keys_module_obj):
                    if inspect.isclass(obj) and issubclass(obj, EnvironmentKey) and \
                            obj != EnvironmentKey:
                        if cls_name == "Observation":
                            env_keys = env_state.keys_obs
                        else:
                            # class naming scheme is enforced in EnvironmentKey construction
                            assert cls_name == "Evidence"
                            env_keys = env_state.keys_ev

                        for key_name, member in obj.__members__.items():
                            self._key_id_by_name[member.key_full_name()] = member.value
                            self._key_by_id[member.value] = member

                            env_keys.add(member)  # attribute of EnvState

                            self._env_state_by_key[member] = env_state

        if len(self._env_state):
            env_names = []
            for env_state in self._env_state:
                obs_names = env_state.obs_key_names
                if not len(obs_names):
                    obs_names.append("<none>")

                ev_names = env_state.ev_key_names
                if not len(ev_names):
                    ev_names.append("<none>")

                env_names.append(f"{env_state.full_name} [obs keys: {', '.join(obs_names)}, "
                                 f"ev keys: {', '.join(ev_names)}]")

            logger.info("%d environments are loaded: %s", len(env_names), ', '.join(env_names))
        else:
            logger.warning("No environments available to load")

    def _env_tell_to(self, from_env: EnvState, obs_key: EnvironmentKey, obs_val: ENV_KEY_TYPE) -> None:
        """Give an observation to environment according to observation key."""
        self.logger_dist.debug("New observation (env -> env) from environment '%s': key %s, value: %s",
                               from_env.full_name, obs_key.key_full_name(), str(obs_val))

        try:
            env_state = self._env_state_by_key[obs_key]
        except KeyError:
            raise NetEnvError(f"environment key '{obs_key.key_full_name()}' does not have an "
                              "environment associated to it")

        if obs_key not in env_state.keys_obs:
            raise NetEnvError(f"environment key '{obs_key.key_full_name()}' is not a valid "
                              f"observation key for environment {env_state.full_name} "
                              f"(observation from {from_env.full_name})")

        env_state.env_update_evidence(0, obs_key, obs_val)

    def _env_ask_from(self, from_env: EnvState, ev_key: EnvironmentKey) -> ENV_KEY_TYPE:
        """Ask for evidence from environment according to evidence key."""
        self.logger_dist.debug("Evidence request (env -> env) from environment '%s': key: %s",
                               from_env.full_name, ev_key.key_full_name())

        try:
            env_state = self._env_state_by_key[ev_key]
        except KeyError:
            raise NetEnvError(f"environment key '{ev_key.key_full_name()}' does not have an "
                              "environment associated to it")

        if ev_key not in env_state.keys_ev:
            raise NetEnvError(f"environment key '{ev_key.key_full_name()}' is not a valid evidence "
                              f"key for environment {env_state.full_name} (evidence request from "
                              f"{from_env.full_name})")

        return env_state.env_get_evidence(0, ev_key)

    # network handlers
    def env_handle_envkey_id_req(self, node_id: int, env_key_name_bytes: bytes) -> Tuple[int]:
        """Return environment key ID corresponding to given env key name."""
        env_key_name = env_key_name_bytes.decode()

        try:
            env_key_id = self._key_id_by_name[env_key_name]
        except KeyError:
            raise NetworkHandlerError(f"environment key '{env_key_name}' does not exist")

        self.logger_dist.debug("Node %d requested id for environment key '%s'",
                               node_id, env_key_name)

        return env_key_id,

    def env_handle_new_obs(self, node_id: int, service_id: int, obs_key_id: int, obs_val_packed: bytes) -> tuple:
        """Given an observation, update the environments to which the keys correspond (Tell)."""
        try:
            obs_key = self._key_by_id[obs_key_id]
        except KeyError:
            raise NetworkHandlerError(f"environment observation key id '{obs_key_id}' not found "
                                      f"(node id: {node_id}, service id: {service_id})")

        num_obs: int = struct.unpack_from(">L", obs_val_packed)[0]
        obs_val: Tuple = struct.unpack_from(f">{obs_key.key_list_type * num_obs}", obs_val_packed, offset=TYPE_LEN_INT)

        self.logger_dist.debug("New observation from node %d, service instance %d: key: %s, value: %s",
                               node_id, service_id, obs_key.key_full_name(), str(obs_val))

        env_state = self._env_state_by_key[obs_key]  # key will exist as an id mapping exists for it

        if obs_key not in env_state.keys_obs:
            raise NetworkHandlerError(f"environment key '{obs_key.key_full_name()}' is not a valid "
                                      f"observation key for environment {env_state.full_name}")

        try:
            env_state.env_update_evidence(node_id, obs_key, obs_val)
        except NetEnvError as ex:
            raise NetworkHandlerError(str(ex))

        return ()

    def env_handle_ev_request(self, node_id: int, service_id: int, ev_key_id: int) -> Tuple[bytes]:
        """Given an evidence key, fetch evidence (Ask)."""
        try:
            ev_key = self._key_by_id[ev_key_id]
        except KeyError:
            raise NetworkHandlerError(f"environment evidence key id '{ev_key_id}' not found "
                                      f"(node id: {node_id}, service id: {service_id})")

        self.logger_dist.debug("New evidence request from node %d, service instance %d: key: %s",
                               node_id, service_id, ev_key.key_full_name())

        env_state = self._env_state_by_key[ev_key]  # key will exist as an id mapping exists for it

        if ev_key not in env_state.keys_ev:
            raise NetworkHandlerError(f"environment key '{ev_key.key_full_name()}' is not a valid "
                                      f"evidence key for environment {env_state.full_name}")

        try:
            ev_val = env_state.env_get_evidence(node_id, ev_key)
        except NetEnvError as ex:
            raise NetworkHandlerError(str(ex)) from ex

        return struct.pack(f">L{ev_key.key_list_type * len(ev_val)}", len(ev_val), *ev_val),
