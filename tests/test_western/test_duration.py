import unittest

import pytest

from neoscore.western.duration import Duration
from neoscore.western.duration_display import DurationDisplay


class TestDuration(unittest.TestCase):
    def test_init_validation(self):
        with pytest.raises(ValueError):
            Duration(-1, 2)
        with pytest.raises(ValueError):
            Duration(-2, 2)
        with pytest.raises(ValueError):
            Duration(0, 2)
        with pytest.raises(ValueError):
            Duration(1, 3)
        with pytest.raises(ValueError):
            Duration(1, 10)
        with pytest.raises(ValueError):
            Duration(1, 0)

    def test_init_fraction_reduced(self):
        duration = Duration(4, 8)
        assert duration.fraction.numerator == 1
        assert duration.fraction.denominator == 2

    def test_from_def(self):
        assert Duration.from_def(Duration(1, 4)) == Duration(1, 4)
        assert Duration.from_def((1, 4)) == Duration(1, 4)

    def test_from_description(self):
        assert Duration.from_description(16, 0) == Duration(1, 16)
        assert Duration.from_description(16, 1) == Duration(3, 32)
        assert Duration.from_description(16, 2) == Duration(7, 64)
        assert Duration.from_description(16, 3) == Duration(15, 128)
        assert Duration.from_description(2, 1) == Duration(3, 4)
        assert Duration.from_description(1, 0) == Duration(1, 1)
        assert Duration.from_description(1, 1) == Duration(3, 2)
        assert Duration.from_description(1, 2) == Duration(7, 4)
        # double breves use base_division 0
        assert Duration.from_description(0, 0) == Duration(2, 1)
        assert Duration.from_description(0, 1) == Duration(3, 1)
        assert Duration.from_description(0, 2) == Duration(7, 2)

    def test_from_description_to_duration_display_always_match(self):
        for base_division in [0, 1, 2, 4, 8, 16, 32, 64]:
            for dot_count in range(0, 5):
                assert Duration.from_description(
                    base_division, dot_count
                ).display == DurationDisplay(base_division, dot_count)

    def test_no_display_with_duration_requiring_tie(self):
        duration = Duration(5, 8)
        assert duration.display is None
        assert duration.requires_tie

    def test_valid_duration_display(self):
        # 16ths with increasing dots
        assert Duration(1, 16).display == DurationDisplay(16, 0)
        assert Duration(3, 32).display == DurationDisplay(16, 1)
        assert Duration(7, 64).display == DurationDisplay(16, 2)
        assert Duration(15, 128).display == DurationDisplay(16, 3)
        # quarters with increasing dots
        assert Duration(1, 4).display == DurationDisplay(4, 0)
        assert Duration(3, 8).display == DurationDisplay(4, 1)
        assert Duration(7, 16).display == DurationDisplay(4, 2)
        assert Duration(15, 32).display == DurationDisplay(4, 3)
        # halfs with increasing dots
        assert Duration(1, 2).display == DurationDisplay(2, 0)
        assert Duration(3, 4).display == DurationDisplay(2, 1)
        assert Duration(7, 8).display == DurationDisplay(2, 2)
        assert Duration(15, 16).display == DurationDisplay(2, 3)
        # wholes with increasing dots
        assert Duration(1, 1).display == DurationDisplay(1, 0)
        assert Duration(3, 2).display == DurationDisplay(1, 1)
        assert Duration(7, 4).display == DurationDisplay(1, 2)
        assert Duration(15, 8).display == DurationDisplay(1, 3)
        # double-breves with increasing dots
        assert Duration(2, 1).display == DurationDisplay(0, 0)
        assert Duration(3, 1).display == DurationDisplay(0, 1)
        assert Duration(7, 2).display == DurationDisplay(0, 2)
        assert Duration(15, 4).display == DurationDisplay(0, 3)

    def test_invalid_duration_display(self):
        # Values < 2 which require ties
        assert Duration(5, 8).display is None
        assert Duration(9, 16).display is None
        assert Duration(11, 16).display is None
        assert Duration(13, 16).display is None
        assert Duration(17, 16).display is None
        assert Duration(18, 16).display is None
        # Values 2 <= x < 4 which require ties
        assert Duration(33, 16).display is None
        assert Duration(35, 16).display is None
        # Values >= 4 (which always require ties)
        assert Duration(4, 1).display is None
        assert Duration(5, 1).display is None
        assert Duration(65, 16).display is None

    def test__float__(self):
        self.assertAlmostEqual(float(Duration(1, 2)), 0.5)

    def test__gt__(self):
        assert Duration(1, 4) > Duration(1, 8)
        assert not (Duration(1, 4) > Duration(3, 8))

    def test__lt__(self):
        assert Duration(1, 4) < Duration(1, 2)
        assert not (Duration(1, 4) < Duration(3, 64))

    def tests__ge__(self):
        assert Duration(1, 4) >= Duration(1, 8)
        assert Duration(1, 4) >= Duration(1, 4)

    def tests__le__(self):
        assert Duration(1, 4) <= Duration(1, 2)
        assert Duration(1, 4) <= Duration(1, 4)

    def test__add__(self):
        assert Duration(1, 4) + Duration(1, 4) == Duration(1, 2)

    def test__sub__(self):
        assert Duration(3, 4) - Duration(1, 4) == Duration(1, 2)
