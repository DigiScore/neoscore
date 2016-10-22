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
