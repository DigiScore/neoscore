import unittest

from brown.core import brown
from brown.core.document import Document
from brown.core.invisible_object import InvisibleObject
from brown.core.paper import Paper
from brown.utils.units import Mm


class TestDocument(unittest.TestCase):

    def test_init_with_explicit_paper(self):
        test_paper = Paper(200, 250, 20, 10, 20, 10, 5)
        test_doc = Document(test_paper)
        assert(test_doc.paper == test_paper)

    def test_page_origin_at_first_page(self):
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(Mm(200), Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc.page_origin(0)
        expected_x = left_margin
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_at_second_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc.page_origin(1)
        page_width = width
        expected_x = (left_margin +
                      page_width + test_doc._page_display_gap)
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_page_origin_at_third_page(self):
        width = Mm(200)
        left_margin = Mm(13)
        top_margin = Mm(21)
        test_paper = Paper(width, Mm(250),
                           top_margin, Mm(10), Mm(20), left_margin, 0)
        test_doc = Document(test_paper)
        found = test_doc.page_origin(2)
        page_width = width
        expected_x = (left_margin +
                      ((page_width + test_doc._page_display_gap) * 2))
        expected_y = top_margin
        self.assertAlmostEqual(found.x, expected_x)
        self.assertAlmostEqual(found.y, expected_y)

    def test_canvas_pos_of(self):
        brown.setup()
        item = InvisibleObject((Mm(5), Mm(6)), brown.document.pages[2])
        canvas_pos = brown.document.canvas_pos_of(item)
        page_pos = brown.document.canvas_pos_of(brown.document.pages[2])
        relative_pos = canvas_pos - page_pos
        self.assertAlmostEqual(Mm(relative_pos.x).value,  Mm(5).value)
        self.assertAlmostEqual(Mm(relative_pos.y).value,  Mm(6).value)
