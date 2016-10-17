import pytest

from brown.named_pitch import NamedPitch
from brown.exceptions import IncompatibleValuesError


def test_init_with_pitch_number_and_letter_success():
    named_pitch = NamedPitch(-11, 'd')
    assert named_pitch.pitch_number == -11
    assert named_pitch.letter == 'd'
    assert named_pitch.accidental.name == 'flat'
    assert named_pitch.octave == -1

def test_init_with_letter_and_accidental_success():
    named_pitch = NamedPitch(pitch_number=20, letter='g', accidental='sharp')
    # Check assignments worked properly
    assert named_pitch.pitch_number == 20
    assert named_pitch.letter == 'g'
    assert named_pitch.accidental.name == 'sharp'
    # Check letter was correctly inferred
    assert named_pitch.octave == 1

def test_init_with_pitch_number_and_accidental_success():
    named_pitch = NamedPitch(pitch_number=22, accidental='sharp')
    # Check assignments worked properly
    assert named_pitch.pitch_number == 22
    assert named_pitch.letter == 'a'
    assert named_pitch.accidental.name == 'sharp'
    # Check letter was correctly inferred
    assert named_pitch.octave == 1

def test_init_with_pitch_num_letter_and_octave_success():
    named_pitch = NamedPitch(pitch_number=20, letter='g', octave=1)
    # Check assignments worked properly
    assert named_pitch.pitch_number == 20
    assert named_pitch.letter == 'g'
    assert named_pitch.octave == 1
    # Check letter was correctly inferred
    assert named_pitch.accidental.name == 'sharp'

def test_init_with_letter_accidental_and_octave_success():
    named_pitch = NamedPitch(letter='g', accidental='sharp', octave=1)
    # Check assignments worked properly
    assert named_pitch.letter == 'g'
    assert named_pitch.accidental.name == 'sharp'
    assert named_pitch.octave == 1
    # Check pitch_number was correctly inferred
    assert named_pitch.pitch_number == 20

def test_init_with_pitch_num_accidental_and_octave_success():
    named_pitch = NamedPitch(pitch_number=20, accidental='sharp', octave=1)
    # Check assignments worked properly
    assert named_pitch.pitch_number == 20
    assert named_pitch.accidental.name == 'sharp'
    assert named_pitch.octave == 1
    # Check letter was correctly inferred
    assert named_pitch.letter == 'g'

def test_init_with_4_good_args_success():
    named_pitch = NamedPitch(pitch_number=13, letter='c', accidental='sharp', octave=1)
    assert named_pitch.pitch_number == 13
    assert named_pitch.letter == 'c'
    assert named_pitch.accidental.name == 'sharp'
    assert named_pitch.octave == 1

def test_init_without_any_args():
    with pytest.raises(TypeError):
        n = NamedPitch()

def test_init_mismatch_pitch_num_and_letter_name():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(5, 'c')

def test_init_mismatch_pitch_num_accidental_and_octave():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=11, accidental='flat', octave=0)

def test_init_mismatch_pitch_num_letter_and_octave():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=12, letter='c', octave=-5)

def test_init_mismatch_pitch_num_letter_and_octave_with_bad_letter_and_pitch():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=12, letter='g', octave=1)

def test_init_mismatch_4_params_bad_pitch_number_and_letter():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=2, letter='g',
                       octave=0, accidental='natural')

def test_init_mismatch_4_params_bad_accidental():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=1, letter='d',
                       octave=0, accidental='sharp')

def test_init_mismatch_4_params_bad_octave():
    with pytest.raises(IncompatibleValuesError):
        n = NamedPitch(pitch_number=1, letter='d',
                       octave=-3, accidental='flat')

def test_init_invalid_letter():
    with pytest.raises(ValueError):
        n = NamedPitch(pitch_number=1, letter='z')

def test_octave_setter_invalid_type():
    named_pitch = NamedPitch(pitch_number=1, letter='d',
                             accidental='flat', octave=0)
    with pytest.raises(TypeError):
        setattr(named_pitch, 'octave', 'fewoifj')

def test_pitch_class_property_calculates_correctly_with_positive_pitch_number():
    named_pitch = NamedPitch(pitch_number=13, letter='d',
                             accidental='flat', octave=1)
    assert named_pitch.pitch_class == 1

def test_pitch_class_property_calculates_correctly_with_negative_pitch_number():
    named_pitch = NamedPitch(pitch_number=-13, letter='b',
                             accidental='natural', octave=-2)
    assert named_pitch.pitch_class == 11

# Still doesn't cover nearly enough for such a complex class
