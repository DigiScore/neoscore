import pytest

from brown.models.pitch import Pitch, InvalidPitchDescriptionError


def test_pitch_init_common_case():
    pitch_string = 'af,,'
    test_pitch = Pitch(pitch_string)
    assert(test_pitch.pitch == pitch_string)
    assert(test_pitch.letter == 'a')
    assert(test_pitch.accidental == 'f')
    assert(test_pitch.octave == 1)


def test_pitch_init_no_letter_fails():
    with pytest.raises(InvalidPitchDescriptionError):
        test_pitch = Pitch('s,')


def test_pitch_init_letter_case_agnostic():
    test_pitch = Pitch('af,,')
    assert(test_pitch.letter == 'a')
    test_pitch_2 = Pitch('Af,,')
    assert(test_pitch_2.letter == 'A')

def test_pitch_init_accidental_case_agnostic():
    test_pitch = Pitch('af,,')
    assert(test_pitch.accidental == 'f')
    test_pitch_2 = Pitch('aF,,')
    assert(test_pitch_2.accidental == 'F')
