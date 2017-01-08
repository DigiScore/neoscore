from fractions import Fraction
import unittest

from nose.tools import assert_raises

from brown.models.duration import Duration, InvalidDurationError


class TestDuration(unittest.TestCase):

    def test_non_nested_is_reduced(self):
        dur = Duration(2, 4)
        assert(dur.numerator == 1)
        assert(dur.denominator == 2)

    def test_nested_is_not_reduced(self):
        dur = Duration(Duration(1, 2), 4)
        assert(isinstance(dur.numerator, Duration))
        assert(dur.numerator.numerator == 1)
        assert(dur.numerator.denominator == 2)
        assert(dur.denominator == 4)

    def test_invalid_duration_caught(self):
        with assert_raises(InvalidDurationError):
            Duration(5, 8)

    def test_properties_are_immutable(self):
        dur = Duration(2, 4)
        with assert_raises(AttributeError):
            dur.numerator = 0
        with assert_raises(AttributeError):
            dur.denominator = 0

    def test__eq__with_non_nested(self):
        assert(Duration(2, 4) == Duration(8, 16))

    def test__ne__with_non_nested(self):
        assert(Duration(2, 4) != Duration(7, 16))

    def test__eq__with_nested(self):
        assert(Duration(Duration(1, 2), 4) == Duration(Duration(2, 4), 4))

    def test__ne__with_nested(self):
        assert(Duration(Duration(1, 2), 4) != Duration(Duration(2, 4), 8))

    def test__repr__(self):
        assert(Duration(Duration(1, 2), 4).__repr__() ==
               'Duration(Duration(1, 2), 4)')

    def test__hash__(self):
        assert({Duration(Duration(1, 2), 4), Duration(Duration(1, 2), 4),
                Duration(Duration(1, 2), 8)} ==
               {Duration(Duration(1, 2), 4), Duration(Duration(1, 2), 8)})

    def test_dot_count(self):
        assert(Duration(1, 4).dot_count == 0)
        assert(Duration(8, 16).dot_count == 0)
        assert(Duration(3, 8).dot_count == 1)
        assert(Duration(7, 16).dot_count == 2)