import unittest

from brown.core import brown
from brown.core.document import Document
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.units import Mm

from tests.mocks.mock_graphic_object import MockGraphicObject


class TestDocument(unittest.TestCase):

    def test_init_with_explicit_paper(self):
        test_paper = Paper(200, 250, 20, 10, 20, 10, 5)
        test_doc = Document(test_paper)
        assert(test_doc.paper == test_paper)

    def test_page_origin_in_canvas_space_at_first_page(self):
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(Mm(200), Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_canvas_space(0)
        expected_x = left_margin
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_in_canvas_space_at_second_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_canvas_space(1)
        page_width = width
        expected_x = (left_margin +
                      page_width + test_doc._page_display_gap)
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_in_canvas_space_at_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc._page_origin_in_canvas_space(2)
        page_width = width
        expected_x = (left_margin +
                      ((page_width + test_doc._page_display_gap) * 2))
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_pos_to_doc_on_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        doc_pos = test_doc._map_to_canvas(Point(Mm(10), Mm(11), 2))
        expected_x = (left_margin +
                      ((width + test_doc._page_display_gap) * 2)) + Mm(10)
        expected_y = top_margin + Mm(11)
        assert(doc_pos == Point(expected_x, expected_y))

    def test_doc_pos_of(self):
        brown.setup()
        item = MockGraphicObject((5, 6, 2))
        relative_pos = Document.doc_pos_of(item)
        assert(relative_pos.x.value == 5)
        assert(relative_pos.y.value == 6)
        assert(relative_pos.page == 2)

    def test_doc_pos_of_through_parent(self):
        brown.setup()
        parent = MockGraphicObject((100, 101))
        item = MockGraphicObject((5, 6), parent=parent)
        relative_pos = Document.doc_pos_of(item)
        assert(relative_pos.x.value == 105)
        assert(relative_pos.y.value == 107)
