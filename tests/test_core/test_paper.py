import unittest

from brown.utils.units import Mm, Inch
from brown.core.paper import Paper


class TestPaper(unittest.TestCase):

    def test_init(self):
        test_paper = Paper(*[Mm(val) for val in [1, 2, 3, 4, 5, 6, 7]])
        assert(test_paper.width == 1)
        assert(test_paper.height == 2)
        assert(test_paper.margin_top == 3)
        assert(test_paper.margin_right == 4)
        assert(test_paper.margin_bottom == 5)
        assert(test_paper.margin_left == 6)
        assert(test_paper.gutter == 7)

    def test_from_template(self):
        test_paper = Paper.from_template('Letter')
        # 'Letter': [Inch(val) for val in [8.5, 11, 1, 1, 1, 1, 0.3]]
        assert(test_paper.width == Inch(8.5))
        assert(test_paper.height == Inch(11))
        assert(test_paper.margin_top == Inch(1))
        assert(test_paper.margin_right == Inch(1))
        assert(test_paper.margin_bottom == Inch(1))
        assert(test_paper.margin_left == Inch(1))
        assert(test_paper.gutter == Inch(0.3))

    def test_live_width(self):
        test_paper = Paper(*[Mm(val) for val in
                             [210, 297, 20, 30, 20, 30, 15]])
        assert(test_paper.live_width == 210 - 30 - 30 - 15)

    def test_live_height(self):
        test_paper = Paper(*[Mm(val) for val in
                             [210, 297, 20, 30, 20, 30, 15]])
        assert(test_paper.live_height == 297 - 20 - 20)
