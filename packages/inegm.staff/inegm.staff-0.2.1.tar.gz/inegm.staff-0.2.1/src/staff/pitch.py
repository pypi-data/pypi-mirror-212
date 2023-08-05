"""Frequency and MIDI pitch representations."""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from functools import total_ordering
from math import floor, log2
from typing import Callable, Optional, Union


@dataclass(frozen=True)
class Diapason:
    """Tuning reference.

    Args:
        reference_midi_number: The reference pitch MIDI number
        reference_hertz: The frequency of the reference pitch in Hertz
    """

    reference_midi_number: int = 69
    reference_hertz: float = 440.0

    def __post_init__(self):
        if (self.reference_midi_number < 0) or (self.reference_midi_number > 127):
            raise ValueError(f"invalid MIDI note number `{self.reference_midi_number}`")

        if self.reference_hertz <= 0:
            raise ValueError(f"invalid Hertz value `{self.reference_hertz}`")


@total_ordering
@dataclass(frozen=True)
class Frequency:
    """Frequency representation.

    Args:
        hertz: The frequency in Hertz (cycles-per-second)

    Implements `total_ordering` against `Frequency`.

    Implements the following operations:

        - `__add__` against `Frequency`
        - `__sub__` against `Frequency`
        - `__mul__` against `int` and `float`
        - `__rmul__` against `int` and `float`
        - `__truediv__` against `int` and `float`
        - `__floor_div__` against `int` and `float`
        - `__round__`

    Implements total ordering.

    Examples:
        Converting to a `MIDIPitch`:

        >>> Frequency(hertz=440).to_midi()
        MIDIPitch(number=69, bend=MIDIBend(bend=0, bend_range=200))

        >>> Frequency(hertz=450).to_midi()
        MIDIPitch(number=69, bend=MIDIBend(bend=1594, bend_range=200))

        The distance between two `Frequency` instances (exponential) in `Cents`
        (linear):

        >>> Frequency(880).cents_distance(Frequency(440))
        Cents(cents=-1200.0)

        >>> round(Frequency(440).cents_distance(Frequency(660)), 2)
        Cents(cents=701.96)

        Adding `Cents` (linear) to `Frequency` (exponential):

        >>> Frequency(40).plus_cents(Cents(2400))
        Frequency(hertz=160.0)

        >>> round(Frequency(40).plus_cents(Cents(2401)), 2)
        Frequency(hertz=160.09)

        `Frequency` arithmetic is simple:

        >>> Frequency(hertz=440) + Frequency(hertz=220)
        Frequency(hertz=660)

        >>> Frequency(hertz=660) - Frequency(hertz=220)
        Frequency(hertz=440)

        >>> Frequency(hertz=440) * 2
        Frequency(hertz=880)

        >>> Frequency(hertz=440) / 2
        Frequency(hertz=220.0)

        >>> round(Frequency(hertz=261.6255653005986), 2)
        Frequency(hertz=261.63)

        As is comparison:

        >>> Frequency(220) > Frequency(110)
        True
    """

    hertz: float

    def __post_init__(self):
        if self.hertz <= 0:
            raise ValueError(f"hertz must be greater than 0. Got {self.hertz}")

    def to_midi(
        self,
        midi_bend_range: int = 200,
        diapason: Diapason = Diapason(),
        octave_divs: int = 12,
    ) -> MIDIPitch:
        """Frequency to MIDIPitch conversion."""
        midi_float = (
            octave_divs * log2(self.hertz / diapason.reference_hertz)
            + diapason.reference_midi_number
        )
        try:
            bend = Cents(100 * divmod(midi_float, int(midi_float))[1]).to_midi_bend(
                bend_range=midi_bend_range
            )
        except ZeroDivisionError:
            # MIDI note 0
            bend = Cents(100 * midi_float).to_midi_bend(bend_range=midi_bend_range)
        return MIDIPitch(
            number=floor(midi_float),
            bend=bend,
            diapason=diapason,
            octave_divs=octave_divs,
        )

    def cents_distance(self, other: Frequency) -> Cents:
        """Cents distance between two frequencies."""
        if not isinstance(other, Frequency):
            raise TypeError("other must be an instance of Frequency.")
        return Cents((1200 * log2(other.hertz / self.hertz)))

    def plus_cents(self, cents: Cents) -> Frequency:
        """Frequency cents distance away."""
        if not isinstance(cents, Cents):
            raise TypeError("cents must be an instance of Cents.")
        return Frequency(hertz=self.hertz * 2 ** (cents.proportion_of_octave))

    def __gt__(self, other: Frequency) -> bool:
        if not isinstance(other, Frequency):
            raise TypeError(f"cannot compare Frequency with type '{type(other)}'")
        return self.hertz > other.hertz

    def _operate(
        self,
        other: Union[int, float],
        oper: Callable,
    ) -> Frequency:
        return Frequency(hertz=oper(self.hertz, other))

    def __add__(self, other: Frequency) -> Frequency:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Frequency' and '{type(other)}'"
            )
        return Frequency(self.hertz + other.hertz)

    def __sub__(self, other: Frequency) -> Frequency:
        if not isinstance(other, Frequency):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Frequency' and '{type(other)}'"
            )
        return Frequency(self.hertz - other.hertz)

    def __mul__(self, other: Union[int, float]) -> Frequency:
        return self._operate(other, operator.mul)

    def __rmul__(self, other: Union[int, float]) -> Frequency:
        return self._operate(other, operator.mul)

    def __truediv__(self, other: Union[int, float]) -> Frequency:
        return self._operate(other, operator.truediv)

    def __floordiv__(self, other: Union[int, float]) -> Frequency:
        return self._operate(other, operator.floordiv)

    def __round__(self, ndigits: int) -> Frequency:
        return Frequency(hertz=round(self.hertz, ndigits))


@total_ordering
@dataclass(frozen=True)
class Cents:
    """Cents representation.

    Args:
        cents: The cents value. There are 1200 cents per octave.

    Implements the following operations:

        - `__add__` against `Cents`
        - `__sub__` against `Cents`
        - `__mul__` against `int` and `float`
        - `__rmul__` against `int` and `float`
        - `__truediv__` against `int` and `float` (though the result is rounded
            to the **closest** int)
        - `__floor_div__` against `int` and `float`

    Implements total ordering.

    Examples:
        `Cents` as a proportion of the octave:

        >>> Cents(600).proportion_of_octave
        0.5

        `Cents` can be converted to `MIDIBend`:

        >>> Cents(1.96).to_midi_bend()
        MIDIBend(bend=80, bend_range=200)

        >>> Cents(-15.64).to_midi_bend()
        MIDIBend(bend=-641, bend_range=200)

        `Cents` arithmetic is simple:

        >>> Cents(100) + Cents(500)
        Cents(cents=600)

        >>> Cents(600) - Cents(100)
        Cents(cents=500)

        >>> Cents(600) * 2
        Cents(cents=1200)

        >>> Cents(1200) / 2
        Cents(cents=600)

        >>> round(Cents(1.96), 0)
        Cents(cents=2.0)

        As is comparison:
        >>> Cents(600) > Cents(100)
        True
    """

    cents: float

    @property
    def proportion_of_octave(self) -> float:
        """Ratio of these cents against a standard 1200 cent octave.

        Returns:
            The proportion (ratio) of these cents against the 1200 cent octave
        """
        return self.cents / 1200.0

    def to_midi_bend(self, bend_range: int = 200) -> MIDIBend:
        """MIDI bend value required to achieve these cents.

        Args:
            bend_range: The set pitch-bend range

        Returns:
            The MIDIBend equivalent of these cents
        """
        return MIDIBend(
            bend=round((8192 / bend_range) * self.cents),
            bend_range=bend_range,
        )

    def __gt__(self, other: Cents) -> bool:
        if not isinstance(other, Cents):
            raise TypeError(f"cannot compare Cents with type '{type(other)}'")
        return self.cents > other.cents

    def _operate(
        self,
        other: Union[int, float],
        oper: Callable,
    ) -> Cents:
        if not isinstance(other, (int, float)):
            raise TypeError(
                f"unsupported operand type(s) for {oper.__name__}: "
                f"'Cents' and '{type(other)}'"
            )
        return Cents(cents=round(oper(self.cents, other)))

    def __add__(self, other: Cents) -> Cents:
        if not isinstance(other, Cents):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Cents' and '{type(other)}'"
            )
        return Cents(self.cents + other.cents)

    def __sub__(self, other: Cents) -> Cents:
        if not isinstance(other, Cents):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Cents' and '{type(other)}'"
            )
        return Cents(self.cents - other.cents)

    def __mul__(self, other: Union[int, float]) -> Cents:
        return self._operate(other, operator.mul)

    def __rmul__(self, other: Union[int, float]) -> Cents:
        return self._operate(other, operator.mul)

    def __truediv__(self, other: Union[int, float]) -> Cents:
        return self._operate(other, operator.truediv)

    def __floordiv__(self, other: Union[int, float]) -> Cents:
        return self._operate(other, operator.floordiv)

    def __round__(self, ndigits: Optional[int] = None) -> Cents:
        return Cents(cents=round(self.cents, ndigits))


@dataclass(frozen=True)
class MIDIBend:
    """MIDI bend value with bend wheel range.

    Args:
        bend: MIDI pitch bend value (in range -8192, 8192)
        bend_range: MIDI bend wheel range in cents. Typically 200 (2 semitones),
            but with some MPE instruments and controllers the bend range is set
            to 2400 (24 semitones).
    """

    bend: int = 0
    bend_range: int = 200

    def __post_init__(self):
        if (self.bend < -8192) or (self.bend > 8192):
            raise ValueError(f"bend must be between -8192 and 8192. Got {self.bend}")

        if self.bend_range <= 0:
            raise ValueError(
                f"bend_range must be greater than 0. Got {self.bend_range}"
            )

    @property
    def cents(self) -> Cents:
        """Get this MIDI bend value as cents.

        Returns:
            The MIDIBend as cents
        """
        return Cents((self.bend / 8192) * self.bend_range)


@total_ordering
@dataclass(frozen=True, repr=False)
class MIDIPitch:
    """MIDI pitch representation which includes pitch-bend.

    Args:
        number: MIDI note number.
        bend: MIDI pitch-wheel bend.
        diapason: Tuning reference.
        octave_divs: Equal divisions of the octave. Typically 12.

    Implements total ordering.

    Examples:
        `MIDIPitches` can be initialized using a string:

        >>> MIDIPitch.from_string("c4")
        MIDIPitch(number=60, bend=MIDIBend(bend=0, bend_range=200))

        >>> MIDIPitch.from_string("c#4")
        MIDIPitch(number=61, bend=MIDIBend(bend=0, bend_range=200))

        >>> MIDIPitch.from_string("db4")
        MIDIPitch(number=61, bend=MIDIBend(bend=0, bend_range=200))

        or a number:

        >>> MIDIPitch(60)
        MIDIPitch(number=60, bend=MIDIBend(bend=0, bend_range=200))

        They can be converted to `Frequency`:

        >>> round(MIDIPitch(60).frequency, 2)
        Frequency(hertz=261.63)

        A `Diapason` can be used to set tuning:

        >>> diapason = Diapason(reference_midi_number=69, reference_hertz=438)
        >>> pitch = MIDIPitch(60, diapason=diapason)
        >>> round(pitch.frequency, 2)
        Frequency(hertz=260.44)

        Octave divisions other than 12 can be used, changing the MIDI note key
        mapping:

        >>> round(MIDIPitch(60, octave_divs=24).frequency, 2)
        Frequency(hertz=339.29)

        Given a pitch that isn't twelve-tone equal-temperament, a `MIDIBend`
        will be applied (note that `Frequency.to_midi` returns a `MIDIPitch`):

        >>> Frequency(100).to_midi().bend
        MIDIBend(bend=1433, bend_range=200)

        They can be compared:

        >>> MIDIPitch.from_string("c#4") == MIDIPitch.from_string("db4")
        True
    """

    number: int
    bend: MIDIBend = MIDIBend(bend=0, bend_range=200)
    diapason: Diapason = Diapason()
    octave_divs: int = field(default=12, compare=False)

    def __post_init__(self):
        if (self.number < 0) or (self.number > 127):
            raise ValueError(f"number must be between 0 and 127. Got {self.number}")

    def __repr__(self):
        return f"MIDIPitch(number={self.number}, bend={self.bend})"

    @property
    def frequency(self) -> Frequency:
        """Convert MIDIPitch to Frequency.

        Returns:
            The MIDIPitch frequency
        """
        fhz = Frequency(
            2
            ** ((self.number - self.diapason.reference_midi_number) / self.octave_divs)
            * self.diapason.reference_hertz
        )
        if self.bend == MIDIBend(bend=0):
            return fhz
        cents = self.bend.cents
        return fhz.plus_cents(cents=cents)

    @classmethod
    def from_string(cls, pitch: str, c4_number: int = 60) -> MIDIPitch:
        """Create a MIDIPitch from a string representations.

        Pitch strings are written as a combination of the pitch note class letter,
        a maximum of one accidental, and an integer representing the octave.
        Sharps are represented by the '#' symbols and flats by 'b'.

        Args:
            pitch: The pitch in string representation.
            c4_number: The MIDI number representing C4.

        Raises:
            ValueError: if an invalid pitch string is given.
        """
        if not isinstance(pitch, str):
            raise TypeError("pitch must be expressed as a 'str'")
        if not isinstance(c4_number, int):
            raise TypeError("c4_number must be expressed as a 'int'")

        pitches = [
            ["b#", "c"],
            ["c#", "db"],
            ["d"],
            ["d#", "eb"],
            ["e", "fb"],
            ["f", "e#"],
            ["f#", "gb"],
            ["g"],
            ["g#", "ab"],
            ["a"],
            ["a#", "bb"],
            ["b", "cb"],
        ]
        pitch = pitch.strip().lower()
        idx = 1
        while pitch[-idx].isnumeric():
            idx += 1
        idx -= 1
        if pitch[-(idx + 1)] == "-":
            idx += 1
        octave = int(pitch[-idx:])
        pitch_class = pitch[:-idx]
        found = False
        pc_number = 0
        for idx, enharmonics in enumerate(pitches):
            if pitch_class in enharmonics:
                pc_number = idx
                found = True
                break
        if not found:
            raise ValueError(f"invalid pitch string : {pitch}")
        if pitch_class == "b#":
            octave += 1
        elif pitch_class == "cb":
            octave -= 1
        return MIDIPitch((c4_number + pc_number) + (octave - 4) * 12)

    def __gt__(self, other: MIDIPitch) -> bool:
        if not isinstance(other, MIDIPitch):
            raise TypeError(f"cannot compare MIDIPitch with type '{type(other)}'")
        return self.frequency > other.frequency
