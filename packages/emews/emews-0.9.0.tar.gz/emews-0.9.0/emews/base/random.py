"""RNGs."""
import importlib
import random


class UniformInt:
    """Samples from a bounded discrete uniform distribution, [lower_bound, upper_bound]."""

    __slots__ = ('lower_bound', 'upper_bound')

    def __init__(self, lower_bound=0, upper_bound=1):
        """Constructor."""
        super().__init__()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def sample(self):
        """Samples using a bounded uniform distribution."""
        return random.randint(self.lower_bound, self.upper_bound)

    def __str__(self) -> str:
        """Return a string of parameters and their current values."""
        return f"{self.__class__.__name__}: lower_bound={self.lower_bound}, " \
               f"upper_bound={self.upper_bound}"


class TruncnormInt:
    """
    Centered truncated discrete normal sampler.

    Mu is defined as the median in [lower_bound, upper_bound].
    """

    __slots__ = ('lower_bound', 'upper_bound', 'sigma', '_dist')

    def __init__(self, lower_bound=0, upper_bound=1, sigma=1):
        """Constructor."""
        super().__init__()

        # Import on object construction so scipy.stats isn't loaded if this sampler isn't needed.
        # Note: the memory overhead is substantial - 50mb + additional thread spawning.
        trunc_norm_obj = getattr(importlib.import_module('scipy.stats'), 'truncnorm')

        mu = upper_bound / 2.0
        self._dist = trunc_norm_obj((lower_bound - mu) / sigma, (upper_bound - mu) / sigma,
                                    loc=mu, scale=sigma)

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.sigma = sigma

    def sample(self):
        """Sample from a truncated normal distribution."""
        return int(round(self._dist.rvs(1)[0]))

    def __str__(self) -> str:
        """Return a string of parameters and their current values."""
        return f"{self.__class__.__name__}: lower_bound={self.lower_bound}, " \
               f"upper_bound={self.upper_bound}, sigma={self.sigma}"


class SequentialIterator:
    """
    Iterates through a range of numbers, returning the next number in a sequence.

    Once the last value in the sequence is sampled, that value is returned until the parameters are
    updated, at which point the sequence resets according to the new parameters.
    """

    __slots__ = ('end_value', '_current_value')

    def __init__(self, start_value=0, end_value=1):
        """Constructor."""
        super().__init__()

        self.end_value = end_value
        self._current_value = start_value

    def sample(self):
        """Return the next value sequentially from a list."""
        ret_value = self._current_value

        if self._current_value < self.end_value:
            self._current_value += 1

        return ret_value

    def __str__(self) -> str:
        """Return a string of parameters and their current values."""
        return f"{self.__class__.__name__}: current_value={self._current_value}, " \
               f"end_value={self.end_value}"
