from neoscore.core import neoscore, paper
from neoscore.core.page import Page
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Inch, Unit

from ..helpers import AppTest


class TestPageSupplier(AppTest):
    def test_init(self):
        pg = Page((Unit(1), Unit(2)), neoscore.document, 1, paper.LETTER)
        assert pg.pos == Point(Unit(1), Unit(2))
        assert pg.page_index == 1

    def test_bounding_rect(self):
        pg = Page((Unit(1), Unit(2)), neoscore.document, 1, paper.LETTER)
        assert pg.bounding_rect == Rect(Unit(1), Unit(2), Inch(8.5), Inch(11))
