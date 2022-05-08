from neoscore.core import neoscore, paper
from neoscore.core.directions import DirectionX
from neoscore.core.page import Page
from neoscore.core.point import ORIGIN, Point
from neoscore.core.rect import Rect
from neoscore.core.units import ZERO, Inch, Mm, Unit

from ..helpers import AppTest


class TestPageSupplier(AppTest):
    def test_init(self):
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            1,
            DirectionX.LEFT,
            paper.LETTER,
        )
        assert pg.pos == Point(Unit(1), Unit(2))
        assert pg.index == 1
        assert pg.page_side == DirectionX.LEFT
        assert pg.paper == paper.LETTER

    def test_bounding_rect_for_left_page_with_gutter(self):
        test_paper = paper.LETTER.modified(gutter=Mm(20))
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            DirectionX.LEFT,
            test_paper,
        )
        assert pg.bounding_rect == Rect(Inch(-1), Inch(-1), Inch(8.5), Inch(11))

    def test_bounding_rect_for_right_page_with_gutter(self):
        test_paper = paper.LETTER.modified(gutter=Mm(20))
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            DirectionX.RIGHT,
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
            DirectionX.RIGHT,
            paper.LETTER,
        )
        assert pg.bounding_rect == Rect(Inch(-1), Inch(-1), Inch(8.5), Inch(11))

    def test_document_space_bounding_rect(self):
        pg = Page(
            (Unit(1), Unit(2)),
            neoscore.document,
            0,
            DirectionX.RIGHT,
            paper.LETTER,
        )
        assert pg.document_space_bounding_rect == Rect(
            Inch(-1) + Unit(1), Inch(-1) + Unit(2), Inch(8.5), Inch(11)
        )

    def test_full_margin_left(self):
        test_paper = paper.A4.modified(gutter=Mm(7))
        assert Page(
            ORIGIN, neoscore.document, 0, DirectionX.RIGHT, test_paper
        ).full_margin_left == Mm(27)
        assert Page(
            ORIGIN, neoscore.document, 0, DirectionX.LEFT, test_paper
        ).full_margin_left == Mm(20)

    def test_full_margin_right(self):
        test_paper = paper.A4.modified(gutter=Mm(7))
        assert Page(
            ORIGIN, neoscore.document, 0, DirectionX.RIGHT, test_paper
        ).full_margin_right == Mm(20)
        assert Page(
            ORIGIN, neoscore.document, 0, DirectionX.LEFT, test_paper
        ).full_margin_right == Mm(27)

    def test_left_margin_x(self):
        page = Page(ORIGIN, neoscore.document, 0, DirectionX.RIGHT, paper.A4)
        assert page.left_margin_x == ZERO
        assert page.right_margin_x == paper.A4.live_width
        assert page.top_margin_y == ZERO
        assert page.bottom_margin_y == paper.A4.live_height
        assert page.center_x == paper.A4.live_width / 2
