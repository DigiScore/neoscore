from fractions import Fraction
import unittest

from nose.tools import assert_raises, nottest

from brown.models.beat import Beat
from brown.utils.units import Unit


MockBeat = Beat._make_concrete_beat(100)


class TestBeat(unittest.TestCase):

    def test_init_from_numerator_denominator(self):
        dur = MockBeat(1, 4)
        assert(dur.numerator == 1)
        assert(dur.denominator == 4)

    def test_init_from_existing_beat(self):
        original_dur = MockBeat(1, 4)
        dur = MockBeat(original_dur)
        assert(dur.numerator == 1)
        assert(dur.denominator == 4)

    def test_nested_is_not_reduced(self):
        dur = MockBeat(MockBeat(1, 2), 4)
        assert(isinstance(dur.numerator, MockBeat))
        assert(dur.numerator.numerator == 1)
        assert(dur.numerator.denominator == 2)
        assert(dur.denominator == 4)

    def test_from_float(self):
        assert(MockBeat.from_float(0.4) == MockBeat(2, 5))
        assert(MockBeat.from_float(0.4, limit_denominator=1) == MockBeat(0, 1))
        assert(MockBeat.from_float(0.4, 8) == MockBeat(3, 8))

    @nottest
    def test_requires_tie(self):
        assert(MockBeat(5, 8).requires_tie is True)
        assert(MockBeat(4, 8).requires_tie is False)

    def test_properties_are_immutable(self):
        dur = MockBeat(2, 4)
        with assert_raises(AttributeError):
            dur.numerator = 0
        with assert_raises(AttributeError):
            dur.denominator = 0

    def test__float__(self):
        self.assertAlmostEqual(float(MockBeat(1, 2)), 0.5)

    def test__eq__with_non_nested(self):
        assert(MockBeat(2, 4) == MockBeat(2, 4))

    def test__ne__with_non_nested(self):
        assert(MockBeat(2, 4) != MockBeat(7, 16))

    def test__eq__with_nested(self):
        assert(MockBeat(MockBeat(1, 2), 4) == MockBeat(MockBeat(1, 2), 4))

    def test__ne__with_nested(self):
        assert(MockBeat(MockBeat(1, 2), 4) != MockBeat(MockBeat(2, 4), 8))

    def test__gt__with_non_nested(self):
        assert(MockBeat(1, 4) > MockBeat(1, 8))

    def test__lt__with_non_nested(self):
        assert(MockBeat(1, 4) < MockBeat(1, 2))

    def tests__gte__with_non_nested(self):
        assert(MockBeat(1, 4) >= MockBeat(1, 8))
        assert(MockBeat(1, 4) >= MockBeat(1, 4))

    def tests__lte__with_non_nested(self):
        assert(MockBeat(1, 4) <= MockBeat(1, 2))
        assert(MockBeat(1, 4) <= MockBeat(1, 4))

    def test__gt__with_nested(self):
        assert(MockBeat(MockBeat(1, 1), 4) > MockBeat(MockBeat(1, 2), 4))

    def test__lt__with__nested(self):
        assert(MockBeat(MockBeat(1, 2), 4) < MockBeat(MockBeat(1, 1), 4))

    def tests__gte__with_nested(self):
        assert(MockBeat(1, 4) >= MockBeat(MockBeat(1, 3), 8))
        assert(MockBeat(1, 4) >= MockBeat(MockBeat(1, 1), 4))

    def tests__lte__with_nested(self):
        assert(MockBeat(1, 4) <= MockBeat(MockBeat(1, 1), 1))
        assert(MockBeat(1, 4) <= MockBeat(MockBeat(1, 2), 2))

    def test__hash__(self):
        assert({MockBeat(MockBeat(1, 2), 4), MockBeat(MockBeat(1, 2), 4),
                MockBeat(MockBeat(1, 2), 8)} ==
               {MockBeat(MockBeat(1, 2), 4), MockBeat(MockBeat(1, 2), 8)})

    def test__add__with_non_nested(self):
        assert(MockBeat(1, 4) + MockBeat(1, 4) == MockBeat(1, 2))

    def test__add__with_nested(self):
        assert(MockBeat(MockBeat(1, 2), 4) + MockBeat(1, 4) == MockBeat(3, 8))

    def test__sub__with_non_nested(self):
        assert(MockBeat(3, 4) - MockBeat(1, 4) == MockBeat(1, 2))

    def test__sub__with_nested(self):
        assert(MockBeat(MockBeat(1, 2), 4) - MockBeat(1, 16) == MockBeat(1, 16))

    def test_dot_count(self):
        assert(MockBeat(1, 4).dot_count == 0)
        assert(MockBeat(8, 16).dot_count == 0)
        assert(MockBeat(3, 8).dot_count == 1)
        assert(MockBeat(7, 16).dot_count == 2)

    def test_float_to_rounded_fraction(self):
        assert(Beat._float_to_rounded_fraction_tuple(0.4, 4) == (2, 4))

    def test_collapsed_fraction(self):
        assert(MockBeat(1, 4))._as_collapsed_fraction() == Fraction(1, 4)
        assert(MockBeat(2, 4))._as_collapsed_fraction() == Fraction(1, 2)
        assert(MockBeat(MockBeat(1, 2), 4)._as_collapsed_fraction() == Fraction(1, 8))


class TestBeatInteractionWithUnit(unittest.TestCase):

    # NOTE: for testing purposes, MockBeat(1, 1) == Unit(100),
    #       but in practice the conversion rate will vary from
    #       one concrete Beat class to another

    def test_conversion_to_unit(self):
        assert(Unit(MockBeat(1, 1)) == Unit(100))

    def test_init_from_unit(self):
        assert(MockBeat(Unit(100)) == MockBeat(1, 1))
