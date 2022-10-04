import pytest

from neoscore.core.brush import Brush
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rect import Rect
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.staff import Staff

from ..helpers import AppTest, assert_almost_equal


class TestMusicText(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff((Mm(0), Mm(0)), None, length=Mm(100), line_spacing=Mm(1))
        self.font = MusicFont("Bravura", self.staff.unit)

    def test_init(self):
        pen = Pen("#00ff00")
        brush = Brush("#ff0000")
        mock_parent = PositionedObject((Unit(10), Unit(11)), self.staff)
        mtext = MusicText(
            (Unit(5), Unit(6)),
            mock_parent,
            "accidentalFlat",
            self.font,
            brush,
            pen,
            2,
            123,
            "#00f",
            False,
            AlignmentX.RIGHT,
            AlignmentY.CENTER,
            ORIGIN,
        )
        assert mtext.pos == Point(Unit(5), Unit(6))
        assert mtext.parent == mock_parent
        assert mtext.text == "\ue260"
        assert mtext.font == self.font
        assert mtext.brush == brush
        assert mtext.pen == pen
        assert mtext.scale == 2
        assert mtext.rotation == 123
        assert mtext.background_brush == Brush("#00f")
        assert not mtext.breakable
        assert mtext.alignment_x == AlignmentX.RIGHT
        assert mtext.alignment_y == AlignmentY.CENTER
        assert mtext.transform_origin == ORIGIN

    def test_init_with_one_tuple(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, ("brace", 1))
        assert mtext.text == "\uF400"

    def test_init_with_one_music_char(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), self.staff, MusicChar(self.staff.music_font, "brace", 1)
        )
        assert mtext.text == "\uF400"

    def test_init_with_multiple_chars_in_list(self):
        mtext = MusicText(
            (Unit(5), Unit(6)), self.staff, ["accidentalFlat", ("brace", 1)]
        )
        assert mtext.text == "\ue260\uF400"

    def test_init_with_empty_str(self):
        mtext = MusicText(ORIGIN, self.staff, "")
        assert mtext.text == ""
        assert mtext.music_chars == []
        bounding_rect = mtext.bounding_rect
        assert bounding_rect == Rect(ZERO, ZERO, ZERO, ZERO)

    def test_text_setter(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.text == "\ue262"
        mtext.text = "accidentalFlat"
        assert mtext.text == "\ue260"
        assert mtext.music_chars == [MusicChar(self.font, "accidentalFlat")]

    def test_music_chars_setter(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.music_chars == [MusicChar(self.font, "accidentalSharp")]
        assert mtext.text == "\ue262"
        new_chars = [MusicChar(self.font, "accidentalFlat")]
        mtext.music_chars = new_chars
        assert mtext.music_chars == new_chars
        # text should be updated too
        assert mtext.text == "\ue260"

    def test_breakable_passed_to_superclass(self):
        mtext = MusicText((Unit(5), Unit(6)), self.staff, "accidentalSharp")
        assert mtext.breakable

    @pytest.mark.skip("Bounding rects do not currently respond to rotation")
    def test_bounding_rect_responds_to_rotation(self):
        # Documenting this functionality gap
        mtext = MusicText(ORIGIN, self.staff, "accidentalSharp")
        original = mtext.bounding_rect
        mtext.rotation = 90
        rotated = mtext.bounding_rect
        assert rotated.width == original.height
        assert rotated.height == original.width

    def test_bounding_rect_with_centering(self):
        obj = MusicText(ORIGIN, self.staff, "accidentalSharp")
        uncentered_rect = obj.bounding_rect
        obj.alignment_x = AlignmentX.CENTER
        obj.alignment_y = AlignmentY.CENTER
        centered_rect = obj.bounding_rect
        assert centered_rect.width == uncentered_rect.width
        assert centered_rect.height == uncentered_rect.height
        assert_almost_equal(centered_rect.x, Unit(-2), epsilon=2)
        assert_almost_equal(centered_rect.y, Unit(-4), epsilon=2)
