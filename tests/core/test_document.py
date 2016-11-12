import unittest
import pytest

from brown.core import brown
from brown.utils import units
from brown.core.document import Document
from brown.core.paper import Paper


class TestDocument(unittest.TestCase):

    def test_init_with_explicit_paper(self):
        test_paper = Paper(200, 250, 20, 10, 20, 10, 5)
        test_doc = Document(test_paper)
        assert(test_doc.paper == test_paper)

    def test_init_with_default_paper(self):
        # Default value in config is
        # {'A4': (210, 297, 20, 20, 20, 20, 10)}
        # Should this be mocked?
        test_doc = Document()
        assert(test_doc.paper.width == 210)
        assert(test_doc.paper.height == 297)
        assert(test_doc.paper.margin_top == 20)
        assert(test_doc.paper.margin_right == 20)
        assert(test_doc.paper.margin_bottom == 20)
        assert(test_doc.paper.margin_left == 20)
        assert(test_doc.paper.gutter == 10)

    def test_page_origin_in_doc_space_at_first_page(self):
        left_margin = 13
        top_margin = 21
        test_paper = Paper(200, 250, top_margin, 10, 20, left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(1)
        expected_x = left_margin * units.mm
        expected_y = top_margin * units.mm
        self.assertAlmostEqual(found[0], expected_x)
        self.assertAlmostEqual(found[1], expected_y)

    def test_page_origin_in_doc_space_at_second_page(self):
        width = 200
        left_margin = 13
        top_margin = 21
        test_paper = Paper(width, 250, top_margin, 10, 20, left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(2)
        page_width = width * units.mm
        expected_x = ((left_margin * units.mm) +
                      page_width + test_doc._page_display_gap)
        expected_y = top_margin * units.mm
        self.assertAlmostEqual(found[0], expected_x)
        self.assertAlmostEqual(found[1], expected_y)

    def test_page_origin_in_doc_space_at_third_page(self):
        width = 200
        left_margin = 13
        top_margin = 21
        test_paper = Paper(width, 250, top_margin, 10, 20, left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_doc_space(3)
        page_width = width * units.mm
        expected_x = ((left_margin * units.mm) +
                      ((page_width + test_doc._page_display_gap) * 2))
        expected_y = top_margin * units.mm
        self.assertAlmostEqual(found[0], expected_x)
        self.assertAlmostEqual(found[1], expected_y)

    def test_page_origin_in_doc_space_with_invalid_page_numbers(self):
        test_paper = Paper(200, 250, 20, 10, 20, 10, 0)
        test_doc = Document(test_paper)
        with pytest.raises(ValueError):
            test_doc._page_origin_in_doc_space(0)
        with pytest.raises(ValueError):
            test_doc._page_origin_in_doc_space(-1)
