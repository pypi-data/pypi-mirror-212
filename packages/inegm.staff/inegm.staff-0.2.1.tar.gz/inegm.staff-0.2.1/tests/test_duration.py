from fractions import Fraction
import pytest
from staff import Duration, Tempo, Tuplet


def test_duration_class_initialization():
    Duration(4)
    Duration(1, dots=4)
    with pytest.raises(TypeError):
        Duration(0.25)
    with pytest.raises(TypeError):
        Duration(8.5)
    with pytest.raises(TypeError):
        Duration(8, dots=0.5)
    with pytest.raises(TypeError):
        Duration("dotted quarter")
    with pytest.raises(ValueError):
        Duration(3)


def test_duration_class_comparison():
    assert Duration(4) > Duration(8)
    assert Duration(4) < Duration(4, dots=1)
    assert Duration(4) != 0.25
    with pytest.raises(TypeError):
        Duration(4) >= 0.25


def test_duration_class_decimal():
    assert Duration(4).decimal == 0.25
    assert Duration(4, dots=1).decimal == 0.375


def test_duration_class_fraction():
    assert Duration(4).fraction == Fraction(1, 4)
    assert Duration(4, dots=1).fraction == Fraction(3, 8)


def test_duration_class_to_milliseconds():
    assert Duration(4).milliseconds(Tempo(60)) == 1000.0
    assert Duration(2).milliseconds(Tempo(120)) == 1000.0
    assert Duration(8).milliseconds(Tempo(120)) == 250.0


def test_duration_class_arithmetic():
    assert Duration(4) + Duration(8) == Duration(4, dots=1)
    assert sum((Duration(4), Duration(8), Duration(8))) == Duration(2)
    assert sum((Duration(8), Duration(8), Duration(8))) == Duration(4, dots=1)
    with pytest.raises(ValueError):
        # Results in invalid Duration 39/32
        Duration(4, dots=1) + Duration(4, dots=3)
    assert Duration(4) - Duration(8) == Duration(8)
    assert Duration(4) * 2 == Duration(2)
    assert Duration(4) * 0.5 == Duration(8)
    assert 2 * Duration(4) == Duration(2)
    assert Duration(4) / 2 == Duration(8)
    with pytest.raises(TypeError):
        2 / Duration(4)


def test_tuplet_class_initialization():
    Tuplet(3, Duration(2))
    with pytest.raises(TypeError):
        Tuplet(1.2, Duration(2))
    with pytest.raises(TypeError):
        Tuplet(3, 2)


def test_tuplet_class_to_milliseconds():
    tup = Tuplet(3, Duration(2)).to_milliseconds(Tempo(60))
    assert [round(d) for d in tup] == [667, 667, 667]


def test_tempo_class_initialization():
    Tempo(120)
    Tempo(60, Duration(8))
    with pytest.raises(TypeError):
        Tempo(3.14)
    with pytest.raises(TypeError):
        Tempo("adagio")
