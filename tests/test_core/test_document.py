import unittest

from neoscore.core import paper
from neoscore.core.document import _PAGE_DISPLAY_GAP, Document  # noqa
from neoscore.core.paper import Paper
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm


class TestDocument(unittest.TestCase):
    def test_init_with_explicit_paper(self):
        test_paper = Paper(Mm(200), Mm(250), Mm(20), Mm(10), Mm(20), Mm(10), Mm(5))
        test_doc = Document(test_paper)
        assert test_doc.paper == test_paper

    def test_page_origin(self):
        test_doc = Document(paper.A4)
        assert test_doc.page_origin(0) == ORIGIN
        assert test_doc.page_origin(1) == Point(
            paper.A4.width + _PAGE_DISPLAY_GAP, ZERO
        )
        assert test_doc.page_origin(2) == Point(
            (paper.A4.width + _PAGE_DISPLAY_GAP) * 2, ZERO
        )
