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


def test_pitch_init_letter_case_agnostic():
    test_pitch = Pitch('af,,')
    assert(test_pitch.letter == 'a')
    test_pitch_2 = Pitch('Af,,')
    assert(test_pitch_2.letter == 'A')


def test_pitch_init_accidental_case_agnostic():
    test_pitch = Pitch('af,,')
    assert(test_pitch.accidental.value == -1)
    test_pitch_2 = Pitch('aF,,')
    assert(test_pitch_2.accidental.value == -1)


def test_no_octave_marks():
    assert(Pitch('af').octave == 3)


def test_comma_octave_marks():
    assert(Pitch('af,').octave == 2)


def test_apostrophe_octave_marks():
    assert(Pitch("af'").octave == 4)


def test_pitch_class():
    assert(Pitch('af').pitch_class == 8)
