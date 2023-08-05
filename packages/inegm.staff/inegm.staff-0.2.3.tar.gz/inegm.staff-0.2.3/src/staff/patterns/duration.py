"""Musical duration patterns."""
from __future__ import annotations

import itertools as it
from typing import List, Union

from staff import Duration, Tempo

from .pattern import _BasePattern


class DurationPattern(_BasePattern):
    """Musical duration pattern.

    Implements the following operations:

        - `__hash__`
        - `__len__`
        - `__getitem__`
        - `__mul__` against `float`
        - `__truediv__` against `float`

    Note:
        All operations return a copy, `DurationPattern`s are immutable.
    """

    def __init__(self, pattern: List[Duration]):
        """Initialises a DurationPattern

        Args:
            pattern: The initial pattern

        Raises:
            TypeError: If anything but a Duration is included in the initial list
        """
        for dur in pattern:
            if not isinstance(dur, Duration):
                raise TypeError("DurationPattern can only contain Duration objects")
        self._pat = pattern

    def append(self, value: Duration) -> DurationPattern:
        """Append a duration to the pattern

        Args:
            value: A duration to append

        Raises:
            TypeError: If anything but a Duration is passed in

        Returns:
            A new `DurationPattern` (they are immutable)
        """
        if not isinstance(value, Duration):
            raise TypeError("DurationPattern can only contain Duration objects")
        return DurationPattern([value] + self._pat)

    def prepend(self, value: Duration) -> DurationPattern:
        """Insert a duration value at the start of the pattern.

        Args:
            value: A duration to prepend

        Raises:
            TypeError: If anything but a Duration is passed in

        Returns:
            A new `DurationPattern` (they are immutable)
        """
        if not isinstance(value, Duration):
            raise TypeError("DurationPattern can only contain Duration objects")
        return DurationPattern(self._pat + [value])

    def milliseconds(self, tempo: Tempo) -> float:
        """Total millisecond duration of the pattern.

        Args:
            tempo: The tempo used to measure time

        Returns:
            Total milliseconds
        """
        return sum((dur.milliseconds(tempo) for dur in self._pat))

    def retrograde(self) -> DurationPattern:
        """The pattern's retrograde.

        Returns:
            The pattern's retrograde as a new `DurationPattern` (they are immutable)
        """
        return DurationPattern(pattern=self._pat[::-1])

    def rotate(self, factor: int) -> DurationPattern:
        """Rotates the pattern.

        Args:
            factor: The rotation factor (how many durations to rotate). Can be
                negative to rotate left.

        Raises:
            TypeError: If anything but an `int` is passed for factor

        Returns:
            A new and rotated `DurationPattern` (they are immutable)
        """
        if not isinstance(factor, int):
            raise TypeError("can only rotate by an 'int' factor")
        return DurationPattern(pattern=self._pat[factor:] + self._pat[:factor])

    def prolate(self, factor: Union[int, float]) -> DurationPattern:
        """Stretches or contracts the pattern.

        Args;
            factor: Augment with factor > 1, diminish with 0 < factor < 1

        Returns:
            The prolated pattern (as a copy)
        """
        return self * factor

    def permutations(self) -> List[DurationPattern]:
        return [DurationPattern(list(pat)) for pat in it.permutations(self._pat)]

    def __repr__(self):
        _repr = f"{self.__class__.__name__}(["
        for dur in self._pat:
            _repr += str(dur.denominator)
            _repr += "." * dur.dots
            _repr += "r" if dur.is_rest else ""
            _repr += ", "
        return _repr[:-2] + "])"

    def __mul__(self, other: float) -> DurationPattern:
        return DurationPattern([dur * other for dur in self._pat])

    def __truediv__(self, other: float) -> DurationPattern:
        return DurationPattern([dur / other for dur in self._pat])
