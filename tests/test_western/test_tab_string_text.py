from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Inch, Mm
from neoscore.western.tab_staff import TabStaff
from neoscore.western.tab_string_text import TabStringText

from ..helpers import AppTest


class TestTabClef(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = TabStaff(ORIGIN, None, Mm(200))

    def test_y_position_centered_on_string(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1")
        # Because font sizes flake, can't hard-code expected values here
        assert text.y == self.staff.string_y(1) + (text.bounding_rect.height / 2)

    def test_font_defaults_to_staff(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1")
        assert text.music_font == self.staff.music_font

    def test_font_override(self):
        font = MusicFont("Bravura", Inch)
        text = TabStringText(Mm(10), self.staff, 1, "fingering1", font)
        assert text.music_font == font

    def test_brush_default(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1")
        assert text.brush == Brush()

    def test_brush_override(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1", brush="#ff0000")
        assert text.brush == Brush("#ff0000")

    def test_pen_default_is_no_pen(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1")
        assert text.pen == Pen.no_pen()

    def test_pen_override(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1", pen="#ff0000")
        assert text.pen == Pen("#ff0000")

    def test_background_brush_automatically_set(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1")
        assert text.background_brush == neoscore.background_brush

    def test_background_brush_can_be_disabled(self):
        text = TabStringText(Mm(10), self.staff, 1, "fingering1", hide_background=False)