"""Representation of musical duration and time."""

from __future__ import annotations, division

import operator
from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering
from typing import Callable, Union

from .numerical import is_power_of_two

MAX_DURATION_DENOMINATOR = 64
MAX_DURATION_DOTS = 4
MIN_TEMPO_BPM = 10
MAX_TEMPO_BPM = 300


@total_ordering
@dataclass(frozen=True)
class Duration:
    """Musical duration.

    Args:
        denominator: The 4 in 1/4 for example
        dots: The modifying dots
        is_rest: Is or isn't a silent duration

    Implements `total_ordering` against `Duration`.

    Implements the following operations:

        - `__add__` against `Duration`
        - `__radd__` against `Duration`
        - `__sub__` against `Duration`
        - `__mul__` against `int` and `float`
        - `__rmul__` against `int` and `float`
        - `__truediv__` against `int` and `float`

    Implements total ordering.

    Examples:
        Given a `Tempo`, a `Duration` length in milliseconds is:

        >>> Duration(8, dots=1).milliseconds(Tempo(120))
        375.0

        >>> Duration(8, dots=1).milliseconds(Tempo(60))
        750.0

        `Duration` arithmetic is simple:

        >>> Duration(4) + Duration(8)
        Duration(denominator=4, dots=1, is_rest=False)

        >>> sum((Duration(4), Duration(8), Duration(8)))
        Duration(denominator=2, dots=0, is_rest=False)

        >>> Duration(4) - Duration(8)
        Duration(denominator=8, dots=0, is_rest=False)

        >>> Duration(4) * 2
        Duration(denominator=2, dots=0, is_rest=False)

        >>> Duration(2) / 2
        Duration(denominator=4, dots=0, is_rest=False)

        Notice that adding or substracting two rests returns a rest:

        >>> Duration(4, is_rest=True) + Duration(8, is_rest=True)
        Duration(denominator=4, dots=1, is_rest=True)

        >>> Duration(4, is_rest=True) - Duration(8, is_rest=True)
        Duration(denominator=8, dots=0, is_rest=True)

        but that if one of the two `Duration` instances is not a rest:

        >>> Duration(4, is_rest=True) + Duration(8, is_rest=False)
        Duration(denominator=4, dots=1, is_rest=False)

        >>> Duration(4, is_rest=True) - Duration(8, is_rest=False)
        Duration(denominator=8, dots=0, is_rest=False)

        The same goes for the other operations:

        >>> Duration(4, is_rest=True) * 2
        Duration(denominator=2, dots=0, is_rest=True)

        >>> Duration(2, is_rest=True) / 2
        Duration(denominator=4, dots=0, is_rest=True)

        `Duration` instances are comparable:

        >>> Duration(2) > Duration(4)
        True
    """

    denominator: int
    dots: int = 0
    is_rest: bool = False

    def __post_init__(self):
        if not isinstance(self.denominator, int):
            raise TypeError("denominator must be expressed as an 'int'")

        if self.denominator > MAX_DURATION_DENOMINATOR:
            raise ValueError(f"max denominator is {MAX_DURATION_DENOMINATOR}")

        if self.denominator <= 0:
            raise ValueError("denominator must be greater than 0")

        if not isinstance(self.dots, int):
            raise TypeError("dots must be expressed as an 'int'")

        if self.dots > MAX_DURATION_DOTS:
            raise ValueError(f"max dots is {MAX_DURATION_DOTS}")

        if not is_power_of_two(self.denominator):
            raise ValueError("denominator must be a power of two")

    @property
    def decimal(self) -> float:
        """Get the duration as a decimal value.

        Returns:
            The duration as a decimal
        """
        dec = 1 / self.denominator
        for _dot in range(self.dots):
            dec *= 1.5
        return dec

    @property
    def fraction(self) -> Fraction:
        """Get the duration as a Fraction.

        Returns:
            The duration as a fraction
        """
        return Fraction(self.decimal)

    def milliseconds(self, tempo: Tempo) -> float:
        """Get the duration in milliseconds, given a tempo.

        Args:
            tempo: The tempo used to calculate the duration.

        Returns:
            The duration in milliseconds
        """
        if not isinstance(tempo, Tempo):
            raise TypeError("tempo must be an instance of 'Tempo'")
        return (self.decimal / tempo.beat.decimal) * tempo.beat_milliseconds

    def __gt__(self, other: Duration) -> bool:
        if not isinstance(other, Duration):
            raise TypeError(f"cannot compare Duration with type '{type(other)}'")
        return self.decimal > other.decimal

    def __add__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Duration' and '{type(other)}'"
            )
        try:
            frac = self.fraction + other.fraction
            dots = 0
            while frac.numerator != 1:
                frac = Fraction(frac / 1.5)
                dots += 1
                if dots >= MAX_DURATION_DOTS:
                    raise ValueError
            return Duration(
                frac.denominator,
                dots=dots,
                is_rest=self.is_rest and other.is_rest,
            )
        except ValueError as err:
            frac = self.fraction + other.fraction
            msg = "the + operation would result in the invalid Duration: "
            msg += f"{frac.numerator}/{frac.denominator}"
            raise ValueError(msg) from err

    def __radd__(self, other: Union[int, Duration]) -> Duration:
        if other == 0:
            return self
        if not isinstance(other, Duration):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Duration' and '{type(other)}'"
            )
        return self.__add__(other)

    def __sub__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Duration' and '{type(other)}'"
            )
        try:
            frac = self.fraction - other.fraction
            return Duration(
                frac.denominator,
                is_rest=self.is_rest and other.is_rest,
            )
        except ValueError as err:
            msg = "the - operation would result in an invalid Duration."
            raise ValueError(msg) from err

    def _operate(
        self,
        other: Union[int, float],
        oper: Callable,
    ) -> Duration:
        frac = Fraction(oper(self.fraction, other))
        return Duration(frac.denominator, is_rest=self.is_rest)

    def __mul__(self, other: Union[int, float]) -> Duration:
        return self._operate(other, operator.mul)

    def __rmul__(self, other: Union[int, float]) -> Duration:
        return self._operate(other, operator.mul)

    def __truediv__(self, other: Union[int, float]) -> Duration:
        return self._operate(other, operator.truediv)


@dataclass(frozen=True)
class Tuplet:
    """A duration tuplet (triplet, quintuplet, etc)

    Args:
        divisions: Number of divisions of the total duration
        duration: The tuplet's total duration
    """

    divisions: int
    duration: Duration

    def __post_init__(self):
        if not isinstance(self.divisions, int):
            raise TypeError("divisions must be expressed as an 'int'")

        if not isinstance(self.duration, Duration):
            raise TypeError("duration must be an instance of 'Duration'")

    def to_milliseconds(self, tempo: Tempo):
        """The millisecond duration of each subdivision of the tuplet.

        Args:
            tempo: The tempo used to calculate the duration.
        """
        if not isinstance(tempo, Tempo):
            raise TypeError("tempo must be an instance of 'Tempo'")
        return [
            self.duration.milliseconds(tempo=tempo) / self.divisions
            for _ in range(self.divisions)
        ]


@dataclass(frozen=True)
class Tempo:
    """A musical tempo.

    Args:
        bpm: Beats per minute
        beat: Reference beat duration
    """

    bpm: int
    beat: Duration = Duration(4)

    def __post_init__(self):
        if not isinstance(self.bpm, int):
            raise TypeError("bpm must be expressed as an 'int'")

        if self.bpm < MIN_TEMPO_BPM:
            raise ValueError(f"bpm must be at least {MIN_TEMPO_BPM}")

        if self.bpm > MAX_TEMPO_BPM:
            raise ValueError(f"bpm must be at most {MAX_TEMPO_BPM}")

        if not isinstance(self.beat, Duration):
            raise TypeError("beat must be an instance of 'Duration'")

    @property
    def beat_milliseconds(self) -> float:
        """Get the length of each beat in milliseconds.

        Returns:
            Reference beat duration in milliseconds
        """
        return 60 / self.bpm * 1000
