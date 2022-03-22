import unittest
from fractions import Fraction

import pytest

from neoscore.models.beat import Beat
from neoscore.models.notehead_duration import NoteheadDuration


class TestBeat(unittest.TestCase):
    def test_init_from_numerator_denominator(self):
        dur = Beat(1, 4)
        assert dur.numerator == 1
        assert dur.denominator == 4

    def test_nested_is_not_reduced(self):
        dur = Beat(Beat(1, 2), 4)
        assert isinstance(dur.numerator, Beat)
        assert dur.numerator.numerator == 1
        assert dur.numerator.denominator == 2
        assert dur.denominator == 4

    def test_from_float(self):
        assert Beat.from_float(0.4) == Beat(2, 5)
        assert Beat.from_float(0.4, limit_denominator=1) == Beat(0, 1)
        assert Beat.from_float(0.4, 8) == Beat(3, 8)

    def test_notehead_duration(self):
        assert Beat(1, 4).notehead_duration == NoteheadDuration.SHORT
        assert Beat(3, 8).notehead_duration == NoteheadDuration.SHORT
        assert Beat(1, 256).notehead_duration == NoteheadDuration.SHORT
        assert Beat(1, 2).notehead_duration == NoteheadDuration.HALF
        assert Beat(3, 4).notehead_duration == NoteheadDuration.HALF
        assert Beat(4, 4).notehead_duration == NoteheadDuration.WHOLE
        assert Beat(1, 1).notehead_duration == NoteheadDuration.WHOLE
        assert Beat(3, 2).notehead_duration == NoteheadDuration.WHOLE
        assert Beat(2, 1).notehead_duration == NoteheadDuration.DOUBLE_WHOLE
        assert Beat(3, 1).notehead_duration == NoteheadDuration.DOUBLE_WHOLE

    @pytest.mark.skip
    def test_requires_tie(self):
        assert Beat(5, 8).requires_tie is True
        assert Beat(4, 8).requires_tie is False

    def test_requires_stem(self):
        assert Beat(3, 4).requires_stem is True
        assert Beat(Beat(1, 3), 4).requires_stem is True
        assert Beat(2, 16).requires_stem is True
        assert Beat(2, 2).requires_stem is False
        assert Beat(1, 1).requires_stem is False
        assert Beat(3, 2).requires_stem is False
        assert Beat(2, 1).requires_stem is False

    # noinspection PyPropertyAccess
    def test_properties_are_immutable(self):
        dur = Beat(2, 4)
        with pytest.raises(AttributeError):
            dur.numerator = 0
        with pytest.raises(AttributeError):
            dur.denominator = 0

    def test__float__(self):
        self.assertAlmostEqual(float(Beat(1, 2)), 0.5)

    def test__eq__with_non_nested(self):
        assert Beat(2, 4) == Beat(2, 4)

    def test__ne__with_non_nested(self):
        assert Beat(2, 4) != Beat(7, 16)

    def test__eq__with_nested(self):
        assert Beat(Beat(1, 2), 4) == Beat(Beat(1, 2), 4)

    def test__ne__with_nested(self):
        assert Beat(Beat(1, 2), 4) != Beat(Beat(2, 4), 8)

    def test__gt__with_non_nested(self):
        assert Beat(1, 4) > Beat(1, 8)

    def test__lt__with_non_nested(self):
        assert Beat(1, 4) < Beat(1, 2)

    def tests__gte__with_non_nested(self):
        assert Beat(1, 4) >= Beat(1, 8)
        assert Beat(1, 4) >= Beat(1, 4)

    def tests__lte__with_non_nested(self):
        assert Beat(1, 4) <= Beat(1, 2)
        assert Beat(1, 4) <= Beat(1, 4)

    def test__gt__with_nested(self):
        assert Beat(Beat(1, 1), 4) > Beat(Beat(1, 2), 4)

    def test__lt__with__nested(self):
        assert Beat(Beat(1, 2), 4) < Beat(Beat(1, 1), 4)

    def tests__gte__with_nested(self):
        assert Beat(1, 4) >= Beat(Beat(1, 3), 8)
        assert Beat(1, 4) >= Beat(Beat(1, 1), 4)

    def tests__lte__with_nested(self):
        assert Beat(1, 4) <= Beat(Beat(1, 1), 1)
        assert Beat(1, 4) <= Beat(Beat(1, 2), 2)

    def test__hash__(self):
        assert {Beat(Beat(1, 2), 4), Beat(Beat(1, 2), 4), Beat(Beat(1, 2), 8)} == {
            Beat(Beat(1, 2), 4),
            Beat(Beat(1, 2), 8),
        }

    def test__add__with_non_nested(self):
        assert Beat(1, 4) + Beat(1, 4) == Beat(1, 2)

    def test__add__with_nested(self):
        assert Beat(Beat(1, 2), 4) + Beat(1, 4) == Beat(3, 8)

    def test__sub__with_non_nested(self):
        assert Beat(3, 4) - Beat(1, 4) == Beat(1, 2)

    def test__sub__with_nested(self):
        assert Beat(Beat(1, 2), 4) - Beat(1, 16) == Beat(1, 16)

    def test_dot_count(self):
        assert Beat(1, 4).dot_count == 0
        assert Beat(8, 16).dot_count == 0
        assert Beat(3, 8).dot_count == 1
        assert Beat(7, 16).dot_count == 2
        assert Beat(2, 1).dot_count == 0

    def test_collapsed_fraction(self):
        assert (Beat(1, 4)).to_fraction() == Fraction(1, 4)
        assert (Beat(2, 4)).to_fraction() == Fraction(1, 2)
        assert Beat(Beat(1, 2), 4).to_fraction() == Fraction(1, 8)
