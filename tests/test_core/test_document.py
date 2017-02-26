import unittest
from nose.tools import assert_raises

from brown.utils.point import Point
from brown.utils.units import Mm
from brown.core.document import Document
from brown.core.paper import Paper


class TestDocument(unittest.TestCase):

    def test_init_with_explicit_paper(self):
        test_paper = Paper(200, 250, 20, 10, 20, 10, 5)
        test_doc = Document(test_paper)
        assert(test_doc.paper == test_paper)

    def test_init_with_default_paper(self):
        # Default value in config is
        # 'A4': [Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        # Should this be mocked?
        test_doc = Document()
        assert(test_doc.paper.width == Mm(210))
        assert(test_doc.paper.height == Mm(297))
        assert(test_doc.paper.margin_top == Mm(20))
        assert(test_doc.paper.margin_right == Mm(20))
        assert(test_doc.paper.margin_bottom == Mm(20))
        assert(test_doc.paper.margin_left == Mm(20))
        assert(test_doc.paper.gutter == Mm(10))

    def test_page_origin_in_doc_space_at_first_page(self):
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(Mm(200), Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(1)
        expected_x = left_margin
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_in_doc_space_at_second_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(2)
        page_width = width
        expected_x = (left_margin +
                      page_width + test_doc._page_display_gap)
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_in_doc_space_at_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(3)
        page_width = width
        expected_x = (left_margin +
                      ((page_width + test_doc._page_display_gap) * 2))
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_in_doc_space_with_invalid_page_numbers(self):
        test_paper = Paper(*[Mm(val) for val in [200, 250, 20, 10, 20, 10, 0]])
        test_doc = Document(test_paper)
        with assert_raises(ValueError):
            test_doc._page_origin_in_doc_space(0)
        with assert_raises(ValueError):
            test_doc._page_origin_in_doc_space(-1)

    def test_page_pos_to_doc_on_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        doc_pos = test_doc._page_pos_to_doc(
            Point(10, 11).to_unit(Mm), 3)
        expected_x = (left_margin +
                      ((width + test_doc._page_display_gap) * 2)) + Mm(10)
        expected_y = top_margin + Mm(11)
        assert(doc_pos == Point(expected_x, expected_y))
