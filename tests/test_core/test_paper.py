import unittest
from nose.tools import assert_raises

from brown.core import brown
from brown.utils.units import Mm
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
        # 'A4': [Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        test_paper = Paper.from_template('A4')
        assert(test_paper.width == 210)
        assert(test_paper.height == 297)
        assert(test_paper.margin_top == 20)
        assert(test_paper.margin_right == 20)
        assert(test_paper.margin_bottom == 20)
        assert(test_paper.margin_left == 20)
        assert(test_paper.gutter == 10)

    def test_from_template_is_case_insensitive(self):
        assert(Paper.from_template('A4').__dict__ ==
               Paper.from_template('a4').__dict__)

    def test_live_width(self):
        test_paper = Paper(*[Mm(val) for val in
                             [210, 297, 20, 30, 20, 30, 15]])
        assert(test_paper.live_width == 210 - 30 - 30 - 15)

    def test_live_height(self):
        test_paper = Paper(*[Mm(val) for val in
                             [210, 297, 20, 30, 20, 30, 15]])
        assert(test_paper.live_height == 297 - 20 - 20)
