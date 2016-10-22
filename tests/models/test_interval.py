import pytest
from brown.models.interval import Interval, InvalidIntervalError


def test_interval_direction():
    assert(Interval('am2').direction == 'a')
    assert(Interval('dm2').direction == 'd')


def test_interval_direction_as_int():
    assert(Interval('am2').direction_as_int == 1)
    assert(Interval('dm2').direction_as_int == -1)


def test_interval_quality():
    assert(Interval('am2').quality == 'm')
    assert(Interval('aM2').quality == 'M')
    assert(Interval('ad2').quality == 'd')
    assert(Interval('aA2').quality == 'A')


def test_interval_quality_in_english():
    assert(Interval('am2').quality_in_english == 'minor')
    assert(Interval('aM2').quality_in_english == 'Major')
    assert(Interval('ad2').quality_in_english == 'diminished')
    assert(Interval('aA2').quality_in_english == 'Augmented')


def test_interval_0_distance_fails():
    with pytest.raises(InvalidIntervalError):
        Interval('ad0')


def test_interval_no_direction_fails():
    with pytest.raises(InvalidIntervalError):
        Interval('M2')


def test_interval_no_quality_fails():
    with pytest.raises(InvalidIntervalError):
        Interval('a2')

def test_interval_no_distance_fails():
    with pytest.raises(InvalidIntervalError):
        Interval('aM')

@pytest.mark.skip
def test_interval_pitch_class_delta_major_minor():
    assert(Interval('am2').pitch_class_delta == 1)
    assert(Interval('aM2').pitch_class_delta == 2)
    assert(Interval('am3').pitch_class_delta == 3)
    assert(Interval('aM3').pitch_class_delta == 4)
    assert(Interval('am6').pitch_class_delta == 8)
    assert(Interval('aM6').pitch_class_delta == 9)
    assert(Interval('am7').pitch_class_delta == 10)
    assert(Interval('aM7').pitch_class_delta == 11)
    assert(Interval('dm2').pitch_class_delta == -1)
    assert(Interval('dM2').pitch_class_delta == -2)
    assert(Interval('dm3').pitch_class_delta == -3)
    assert(Interval('dM3').pitch_class_delta == -4)
    assert(Interval('dm6').pitch_class_delta == -8)
    assert(Interval('dM6').pitch_class_delta == -9)
    assert(Interval('dm7').pitch_class_delta == -10)
    assert(Interval('dM7').pitch_class_delta == -11)

@pytest.mark.skip
def test_interval_pitch_class_delta_aug_dim():
    assert(Interval('ad2').pitch_class_delta == 0)
    assert(Interval('aA2').pitch_class_delta == 3)
    assert(Interval('ad3').pitch_class_delta == 2)
    assert(Interval('aA3').pitch_class_delta == 5)
    assert(Interval('ad4').pitch_class_delta == 4)
    assert(Interval('aA4').pitch_class_delta == 6)
    assert(Interval('ad5').pitch_class_delta == 6)
    assert(Interval('aA5').pitch_class_delta == 8)
    assert(Interval('ad6').pitch_class_delta == 7)
    assert(Interval('aA6').pitch_class_delta == 10)
    assert(Interval('ad7').pitch_class_delta == 9)
    assert(Interval('aA7').pitch_class_delta == 12)
