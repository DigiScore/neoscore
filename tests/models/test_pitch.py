import pytest

from brown.models.pitch import Pitch, InvalidPitchDescriptionError


def test_pitch_init_common_case():
    pitch_string = 'af,,'
    test_pitch = Pitch(pitch_string)
    assert(test_pitch.pitch == pitch_string)
    assert(test_pitch.letter == 'a')
    assert(test_pitch.accidental.value == -1)
    assert(test_pitch.octave == 1)


def test_pitch_init_no_letter_fails():
    with pytest.raises(InvalidPitchDescriptionError):
        Pitch('s,')


def test_no_octave_marks():
    assert(Pitch('af').octave == 3)


def test_comma_octave_marks():
    assert(Pitch('af,').octave == 2)


def test_apostrophe_octave_marks():
    assert(Pitch("af'").octave == 4)


def test_pitch_class():
    assert(Pitch('af').pitch_class == 8)

def test_pitch_midi_number():
    assert(Pitch("a''").midi_number == 81)
    assert(Pitch("a'").midi_number == 69)
    assert(Pitch("c'").midi_number == 60)
    assert(Pitch("cf").midi_number == 47)
    assert(Pitch("c").midi_number == 48)
    assert(Pitch("cn").midi_number == 48)
    assert(Pitch("cs").midi_number == 49)
