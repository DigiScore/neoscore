import unittest

from neoscore.core.document import Document
from neoscore.core.paper import Paper
from neoscore.core.point import Point
from neoscore.core.units import Mm

from ..helpers import assert_almost_equal


class TestDocument(unittest.TestCase):
    def test_init_with_explicit_paper(self):
        test_paper = Paper(Mm(200), Mm(250), Mm(20), Mm(10), Mm(20), Mm(10), Mm(5))
        test_doc = Document(test_paper)
        assert test_doc.paper == test_paper

    def test_page_origin_at_first_page(self):
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(
            Mm(200), Mm(250), top_margin, Mm(10), Mm(20), left_margin, Mm(0)
        )
        test_doc = Document(test_paper)
        found = test_doc.page_origin(0)
        assert_almost_equal(found, Point(left_margin, top_margin))

    def test_page_origin_at_second_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(
            width, Mm(250), top_margin, Mm(10), Mm(20), left_margin, Mm(0)
        )
        test_doc = Document(test_paper)
        found = test_doc.page_origin(1)
        page_width = width
        expected_x = left_margin + page_width + test_doc._page_display_gap
        expected_y = top_margin
        assert_almost_equal(found, Point(expected_x, expected_y))

    def test_page_origin_at_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(
            width, Mm(250), top_margin, Mm(10), Mm(20), left_margin, Mm(0)
        )
        test_doc = Document(test_paper)
        found = test_doc.page_origin(2)
        page_width = width
        expected_x = left_margin + ((page_width + test_doc._page_display_gap) * 2)
        expected_y = top_margin
        assert_almost_equal(found, Point(expected_x, expected_y))
