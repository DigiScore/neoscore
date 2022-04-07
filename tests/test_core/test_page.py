from neoscore.core import neoscore, paper
from neoscore.core.directions import HorizontalDirection
from neoscore.core.page import Page
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Inch, Mm, Unit

from ..helpers import AppTest


class TestPageSupplier(AppTest):
    def test_init(self):
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            1,
            HorizontalDirection.LEFT,
            paper.LETTER,
        )
        assert pg.pos == Point(Unit(1), Unit(2))
        assert pg.page_index == 1
        assert pg.page_side == HorizontalDirection.LEFT
        assert pg.paper == paper.LETTER

    def test_bounding_rect_for_left_page_with_gutter(self):
        test_paper = paper.LETTER.modified(gutter=Mm(20))
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            HorizontalDirection.LEFT,
            test_paper,
        )
        assert pg.bounding_rect == Rect(Inch(-1), Inch(-1), Inch(8.5), Inch(11))

    def test_bounding_rect_for_right_page_with_gutter(self):
        test_paper = paper.LETTER.modified(gutter=Mm(20))
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            HorizontalDirection.RIGHT,
            test_paper,
        )
        assert pg.bounding_rect == Rect(
            Inch(-1) - Mm(20), Inch(-1), Inch(8.5), Inch(11)
        )

    def test_bounding_rect_with_no_gutter(self):
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            HorizontalDirection.RIGHT,
            paper.LETTER,
        )
        assert pg.bounding_rect == Rect(Inch(-1), Inch(-1), Inch(8.5), Inch(11))

    def test_document_space_bounding_rect(self):
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            HorizontalDirection.RIGHT,
            paper.LETTER,
        )
        assert pg.document_space_bounding_rect == Rect(
            Inch(-1) + Unit(1), Inch(-1) + Unit(2), Inch(8.5), Inch(11)
        )
