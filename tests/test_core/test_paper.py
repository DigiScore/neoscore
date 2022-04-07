import unittest

from neoscore.core import paper
from neoscore.core.paper import Paper
from neoscore.core.units import Mm


class TestPaper(unittest.TestCase):
    def test_init(self):
        test_paper = Paper(*[Mm(val) for val in [1, 2, 3, 4, 5, 6, 7]])
        assert test_paper.width == Mm(1)
        assert test_paper.height == Mm(2)
        assert test_paper.margin_top == Mm(3)
        assert test_paper.margin_right == Mm(4)
        assert test_paper.margin_bottom == Mm(5)
        assert test_paper.margin_left == Mm(6)
        assert test_paper.gutter == Mm(7)

    def test_live_width(self):
        test_paper = Paper(*[Mm(val) for val in [210, 297, 20, 30, 20, 30, 15]])
        assert test_paper.live_width == Mm(210 - 30 - 30 - 15)

    def test_live_height(self):
        test_paper = Paper(*[Mm(val) for val in [210, 297, 20, 30, 20, 30, 15]])
        assert test_paper.live_height == Mm(297 - 20 - 20)

    def test_make_rotation(self):
        original = Paper(*[Mm(val) for val in [100, 101, 1, 2, 3, 4, 5]])
        rotated = original.make_rotation()
        assert rotated.width == original.height
        assert rotated.height == original.width
        assert rotated.margin_top == original.margin_left
        assert rotated.margin_right == original.margin_top
        assert rotated.margin_bottom == original.margin_right
        assert rotated.margin_left == original.margin_bottom
        assert rotated.gutter == original.gutter

    def test_make_rotation_four_times_no_change(self):
        test_paper = paper.LETTER
        assert (
            test_paper.make_rotation().make_rotation().make_rotation().make_rotation()
            == test_paper
        )

    def test_modifying(self):
        test_paper = Paper(Mm(210), Mm(297), Mm(20), Mm(30), Mm(20), Mm(30), Mm(15))
        assert test_paper.modified(width=Mm(999)) == Paper(
            Mm(999), Mm(297), Mm(20), Mm(30), Mm(20), Mm(30), Mm(15)
        )
        assert test_paper.modified(height=Mm(999)) == Paper(
            Mm(210), Mm(999), Mm(20), Mm(30), Mm(20), Mm(30), Mm(15)
        )
        assert test_paper.modified(margin_top=Mm(1)) == Paper(
            Mm(210), Mm(297), Mm(1), Mm(30), Mm(20), Mm(30), Mm(15)
        )
        assert test_paper.modified(margin_right=Mm(1)) == Paper(
            Mm(210), Mm(297), Mm(20), Mm(1), Mm(20), Mm(30), Mm(15)
        )
        assert test_paper.modified(margin_bottom=Mm(1)) == Paper(
            Mm(210), Mm(297), Mm(20), Mm(30), Mm(1), Mm(30), Mm(15)
        )
        assert test_paper.modified(margin_left=Mm(1)) == Paper(
            Mm(210), Mm(297), Mm(20), Mm(30), Mm(20), Mm(1), Mm(15)
        )
        assert test_paper.modified(gutter=Mm(1)) == Paper(
            Mm(210), Mm(297), Mm(20), Mm(30), Mm(20), Mm(30), Mm(1)
        )
