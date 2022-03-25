import unittest

import pytest

from neoscore.models.beat import Beat
from neoscore.models.beat_display import BeatDisplay


class TestBeat(unittest.TestCase):
    def test_init_validation(self):
        with pytest.raises(ValueError):
            Beat(-1, 2)
        with pytest.raises(ValueError):
            Beat(-2, 2)
        with pytest.raises(ValueError):
            Beat(0, 2)
        with pytest.raises(ValueError):
            Beat(1, 3)
        with pytest.raises(ValueError):
            Beat(1, 10)
        with pytest.raises(ValueError):
            Beat(1, 0)

    def test_init_fraction_reduced(self):
        beat = Beat(4, 8)
        assert beat.fraction.numerator == 1
        assert beat.fraction.denominator == 2

    def test_from_def(self):
        assert Beat.from_def(Beat(1, 4)) == Beat(1, 4)
        assert Beat.from_def((1, 4)) == Beat(1, 4)

    def test_from_description(self):
        assert Beat.from_description(16, 0) == Beat(1, 16)
        assert Beat.from_description(16, 1) == Beat(3, 32)
        assert Beat.from_description(16, 2) == Beat(7, 64)
        assert Beat.from_description(16, 3) == Beat(15, 128)
        assert Beat.from_description(2, 1) == Beat(3, 4)
        assert Beat.from_description(1, 0) == Beat(1, 1)
        assert Beat.from_description(1, 1) == Beat(3, 2)
        assert Beat.from_description(1, 2) == Beat(7, 4)
        # double breves use base_division 0
        assert Beat.from_description(0, 0) == Beat(2, 1)
        assert Beat.from_description(0, 1) == Beat(3, 1)
        assert Beat.from_description(0, 2) == Beat(7, 2)

    def test_from_description_to_beat_display_always_match(self):
        for base_division in [0, 1, 2, 4, 8, 16, 32, 64]:
            for dot_count in range(0, 5):
                assert Beat.from_description(
                    base_division, dot_count
                ).display == BeatDisplay(base_division, dot_count)

    def test_no_display_with_beat_requiring_tie(self):
        beat = Beat(5, 8)
        assert beat.display is None
        assert beat.requires_tie

    def test_valid_beat_display(self):
        # 16ths with increasing dots
        assert Beat(1, 16).display == BeatDisplay(16, 0)
        assert Beat(3, 32).display == BeatDisplay(16, 1)
        assert Beat(7, 64).display == BeatDisplay(16, 2)
        assert Beat(15, 128).display == BeatDisplay(16, 3)
        # quarters with increasing dots
        assert Beat(1, 4).display == BeatDisplay(4, 0)
        assert Beat(3, 8).display == BeatDisplay(4, 1)
        assert Beat(7, 16).display == BeatDisplay(4, 2)
        assert Beat(15, 32).display == BeatDisplay(4, 3)
        # halfs with increasing dots
        assert Beat(1, 2).display == BeatDisplay(2, 0)
        assert Beat(3, 4).display == BeatDisplay(2, 1)
        assert Beat(7, 8).display == BeatDisplay(2, 2)
        assert Beat(15, 16).display == BeatDisplay(2, 3)
        # wholes with increasing dots
        assert Beat(1, 1).display == BeatDisplay(1, 0)
        assert Beat(3, 2).display == BeatDisplay(1, 1)
        assert Beat(7, 4).display == BeatDisplay(1, 2)
        assert Beat(15, 8).display == BeatDisplay(1, 3)
        # double-breves with increasing dots
        assert Beat(2, 1).display == BeatDisplay(0, 0)
        assert Beat(3, 1).display == BeatDisplay(0, 1)
        assert Beat(7, 2).display == BeatDisplay(0, 2)
        assert Beat(15, 4).display == BeatDisplay(0, 3)

    def test_invalid_beat_display(self):
        # Values < 2 which require ties
        assert Beat(5, 8).display == None
        assert Beat(9, 16).display == None
        assert Beat(11, 16).display == None
        assert Beat(13, 16).display == None
        assert Beat(17, 16).display == None
        assert Beat(18, 16).display == None
        # Values 2 <= x < 4 which require ties
        assert Beat(33, 16).display == None
        assert Beat(35, 16).display == None
        # Values >= 4 (which always require ties)
        assert Beat(4, 1).display == None
        assert Beat(5, 1).display == None
        assert Beat(65, 16).display == None

    def test__float__(self):
        self.assertAlmostEqual(float(Beat(1, 2)), 0.5)

    def test__gt__(self):
        assert Beat(1, 4) > Beat(1, 8)
        assert not (Beat(1, 4) > Beat(3, 8))

    def test__lt__(self):
        assert Beat(1, 4) < Beat(1, 2)
        assert not (Beat(1, 4) < Beat(3, 64))

    def tests__ge__(self):
        assert Beat(1, 4) >= Beat(1, 8)
        assert Beat(1, 4) >= Beat(1, 4)

    def tests__le__(self):
        assert Beat(1, 4) <= Beat(1, 2)
        assert Beat(1, 4) <= Beat(1, 4)

    def test__add__(self):
        assert Beat(1, 4) + Beat(1, 4) == Beat(1, 2)

    def test__sub__(self):
        assert Beat(3, 4) - Beat(1, 4) == Beat(1, 2)
