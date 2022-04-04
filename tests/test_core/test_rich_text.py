from neoscore.core import neoscore
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rich_text import RichText
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import ZERO, Mm, Unit

from ..helpers import AppTest, render_scene


class TestRichText(AppTest):
    def setUp(self):
        super().setUp()
        self.html = "<p>test</p>"

    def test_init(self):
        font = neoscore.default_font.modified(size=Unit(20))
        parent = PositionedObject(ORIGIN)
        obj = RichText((Unit(5), Unit(6)), parent, self.html, Unit(100), font, 2)
        assert obj.pos == Point(Unit(5), Unit(6))
        assert obj.parent == parent
        assert obj.html_text == self.html
        assert obj.width == Unit(100)
        assert obj.font == font
        assert obj.scale == 2

    def test_default_font(self):
        obj = RichText((Unit(5), Unit(6)), None, self.html)
        assert obj.font == neoscore.default_font

    def test_length_is_zero(self):
        obj = RichText((Unit(5), Unit(6)), None, self.html)
        assert obj.breakable_length == ZERO

    def test_rich_text_end_to_end(self):
        RichText(ORIGIN, None, "<p>test</p>", Mm(50), None, 2)
        render_scene()
