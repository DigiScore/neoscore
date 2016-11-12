import unittest
import pytest

from brown.core import brown
from brown.core.paper import Paper


class TestPaper(unittest.TestCase):

    def test_init(self):
        test_paper = Paper(1, 2, 3, 4, 5, 6, 7)
        assert(test_paper.width == 1)
        assert(test_paper.height == 2)
        assert(test_paper.margin_top == 3)
        assert(test_paper.margin_right == 4)
        assert(test_paper.margin_bottom == 5)
        assert(test_paper.margin_left == 6)
        assert(test_paper.gutter == 7)

    def test_from_template(self):
        # 'A4': (210, 297, 20, 30, 20, 30, 15)
        test_paper = Paper.from_template('A4')
        assert(test_paper.width == 210)
        assert(test_paper.height == 297)
        assert(test_paper.margin_top == 20)
        assert(test_paper.margin_right == 30)
        assert(test_paper.margin_bottom == 20)
        assert(test_paper.margin_left == 30)
        assert(test_paper.gutter == 15)

    def test_from_template_is_case_insensitive(self):
        Paper.from_template('A4').__dict__ == Paper.from_template('a4').__dict__
