import pytest

from staff import Cents, Frequency, MIDIBend, MIDIPitch


def test_frequency_class_initialization():
    Frequency(440)
    with pytest.raises(ValueError):
        Frequency(hertz=0.0)
    with pytest.raises(TypeError):
        Frequency(hertz="C4")


def test_frequency_class_comparison():
    assert Frequency(hertz=440) == Frequency(hertz=440)
    assert Frequency(hertz=440) < Frequency(hertz=441)


def test_frequency_class_arithmetic():
    assert Frequency(hertz=440) + Frequency(hertz=220) == Frequency(hertz=660)
    with pytest.raises(TypeError):
        220 + Frequency(hertz=440.0)
    assert Frequency(hertz=440) - Frequency(hertz=220) == Frequency(hertz=220)
    with pytest.raises(TypeError):
        880 - Frequency(hertz=440.0)
    assert Frequency(440) / 2 == Frequency(220)
    with pytest.raises(TypeError):
        880 / Frequency(hertz=440.0)
    assert Frequency(hertz=440) // 3 == Frequency(hertz=146.0)
    with pytest.raises(TypeError):
        880 // Frequency(hertz=440.0)
    assert round(Frequency(hertz=440) / 3, 2) == Frequency(hertz=146.67)


def test_frequency_class_to_midi():
    assert Frequency(440).to_midi() == MIDIPitch(69)
    assert Frequency(450).to_midi() == MIDIPitch(69, MIDIBend(1594))
    assert Frequency(8.1758).to_midi() == MIDIPitch(0)


def test_frequency_class_cents_distance():
    with pytest.raises(TypeError):
        Frequency(440).cents_distance(880)
    assert round(Frequency(440).cents_distance(Frequency(660)), 2) == Cents(701.96)
    assert Frequency(440).cents_distance(Frequency(880)) == Cents(1200)
    assert Frequency(880).cents_distance(Frequency(440)) == Cents(-1200)


def test_frequency_class_plus_cents():
    with pytest.raises(TypeError):
        Frequency(440).plus_cents(1200)
    assert round(Frequency(440).plus_cents(Cents(39)), 2) == Frequency(450.02)
    assert Frequency(40).plus_cents(Cents(2400)) == Frequency(160)
    assert round(Frequency(40).plus_cents(Cents(2401)), 2) == Frequency(160.09)
    assert Frequency(220).plus_cents(Cents(-1200)) == Frequency(110)


def test_cents_class_initialization():
    Cents(100)
    Cents(50.73)


def test_cents_class_arithmetic():
    assert Cents(100) + Cents(600) == Cents(700)
    with pytest.raises(TypeError):
        Cents(100) + 600
    assert Cents(100) - Cents(50) == Cents(50)
    with pytest.raises(TypeError):
        Cents(100) - 50
    assert Cents(100) * 2 == 2 * Cents(100) == Cents(200)
    with pytest.raises(TypeError):
        Cents(100) * Cents(2)
    assert Cents(200) / 2 == Cents(100)
    with pytest.raises(TypeError):
        2 / Cents(200)
    assert Cents(201) // 2 == Cents(100)
    with pytest.raises(TypeError):
        2 // Cents(201)
    assert round(Cents(100.12352387)) == Cents(100)


def test_cents_class_to_midi_bend():
    assert Cents(1.96).to_midi_bend() == MIDIBend(80)
    assert Cents(47.41).to_midi_bend() == MIDIBend(1942)
    assert Cents(-15.64).to_midi_bend() == MIDIBend(-641)
    assert Cents(100).to_midi_bend() == MIDIBend(4096)


def test_midi_bend_class_initialization():
    MIDIBend()


def test_midi_bend_class_to_cents():
    assert round(MIDIBend(80).cents, 2) == Cents(1.95)
    assert round(MIDIBend(1942).cents, 2) == Cents(47.41)
    assert round(MIDIBend(-641).cents, 2) == Cents(-15.65)
    assert MIDIBend(4096).cents == Cents(100)


def test_midi_pitch_class_initialization():
    MIDIPitch(60)
    with pytest.raises(ValueError):
        MIDIPitch(number=-1)
    with pytest.raises(ValueError):
        MIDIPitch(number=128)
    with pytest.raises(ValueError):
        MIDIPitch(number=60, bend=MIDIBend(bend=-8193))
    with pytest.raises(ValueError):
        MIDIPitch(number=60, bend=MIDIBend(bend=8193))


def test_midi_pitch_class_comparison():
    assert MIDIPitch(number=60) == MIDIPitch(number=60)
    assert MIDIPitch(number=60) != MIDIPitch(number=58, bend=MIDIBend(8192, 200))
    assert MIDIPitch(number=60) < MIDIPitch(number=61)
    assert MIDIPitch(number=60) < MIDIPitch(number=60, bend=MIDIBend(bend=1))
    assert MIDIPitch(number=60, bend=MIDIBend(bend=1, bend_range=200)) < MIDIPitch(
        number=60, bend=MIDIBend(bend=1, bend_range=2400)
    )


def test_midi_pitch_class_frequency():
    assert MIDIPitch(number=69).frequency == Frequency(hertz=440.0)
    assert round(MIDIPitch(0).frequency, 2) == Frequency(8.18)
    assert MIDIPitch(68, MIDIBend(4096)).frequency == Frequency(440)
    assert MIDIPitch(70, MIDIBend(-4096)).frequency == Frequency(440)


def test_midi_pitch_class_from_string():
    assert MIDIPitch.from_string("C4") == MIDIPitch(60)
    assert MIDIPitch.from_string("C4", c4_number=72) == MIDIPitch(72)
    assert MIDIPitch.from_string("B#4") == MIDIPitch(72)
    assert MIDIPitch.from_string("B#4", c4_number=72) == MIDIPitch(84)
    assert MIDIPitch.from_string("B-1") == MIDIPitch(11)
    with pytest.raises(ValueError):
        MIDIPitch.from_string("mi bémol")
