from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.font import Font
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.text import Text
from neoscore.core.text_alignment import HorizontalAlignment, VerticalAlignment
from neoscore.core.units import ZERO, Unit

from ..helpers import AppTest, assert_almost_equal


class TestText(AppTest):
    def setUp(self):
        super().setUp()
        self.font = Font("Bravura", 12, 1, False)

    def test_init(self):
        pen = Pen("#00ff00")
        brush = Brush("#ff0000")
        mock_parent = PositionedObject((Unit(10), Unit(11)), None)
        obj = Text(
            (Unit(5), Unit(6)),
            mock_parent,
            "testing",
            self.font,
            brush,
            pen,
            2,
            12,
            "#00f",
            3,
            False,
            True,
            True,
        )
        assert obj.x == Unit(5)
        assert obj.y == Unit(6)
        assert obj.text == "testing"
        assert obj.font == self.font
        assert obj.parent == mock_parent
        assert obj.brush == brush
        assert obj.pen == pen
        assert obj.scale == 2
        assert obj.rotation == 12
        assert obj.background_brush == Brush("#00f")
        assert obj.z_index == 3
        assert obj.breakable == False
        assert obj.horizontal_alignment == True
        assert obj.vertical_alignment == True

    def test_default_init_values(self):
        obj = Text((Unit(5), Unit(6)), None, "testing")
        assert obj.font == neoscore.default_font
        assert obj.parent == neoscore.document.pages[0]
        assert obj.brush == Brush()
        assert obj.pen == Pen.no_pen()
        assert obj.scale == 1
        assert obj.background_brush == None
        assert obj.breakable == True

    def test_length_when_non_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=False)
        assert obj.breakable_length == ZERO

    def test_length_when_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        # Can't assert exact length since this can flake
        assert obj.breakable_length == obj.bounding_rect.width

    def test_breakable_setter(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        assert obj.breakable_length == obj.bounding_rect.width
        obj.breakable = False
        assert obj.breakable_length == ZERO

    def test_background_brush(self):
        bg_brush = Brush("#ff0000")
        obj = Text((Unit(5), Unit(6)), None, "testing", background_brush=bg_brush)
        assert obj.background_brush == bg_brush
        obj.background_brush = "#00ffff"
        assert obj.background_brush == Brush("#00ffff")

    def test_rotation(self):
        obj = Text((Unit(5), Unit(6)), None, "testing")
        assert obj.rotation == 0
        obj.rotation = 123
        assert obj.rotation == 123
        assert Text((Unit(5), Unit(6)), None, "testing", rotation=123).rotation == 123

    def test_z_index(self):
        obj = Text((Unit(5), Unit(6)), None, "testing")
        assert obj.z_index == 0
        obj.z_index = 123
        assert obj.z_index == 123
        assert Text((Unit(5), Unit(6)), None, "testing", z_index=123).z_index == 123

    def test_horizontal_alignment_setter(self):
        obj = Text(
            ORIGIN, None, "testing", horizontal_alignment=HorizontalAlignment.CENTER
        )
        assert obj.horizontal_alignment == HorizontalAlignment.CENTER
        obj.horizontal_alignment = HorizontalAlignment.RIGHT
        assert obj.horizontal_alignment == HorizontalAlignment.RIGHT

    def test_vertical_alignment_setter(self):
        obj = Text(ORIGIN, None, "testing", vertical_alignment=VerticalAlignment.CENTER)
        assert obj.vertical_alignment == VerticalAlignment.CENTER
        obj.vertical_alignment = VerticalAlignment.BASELINE
        assert obj.vertical_alignment == VerticalAlignment.BASELINE

    def test_alignment_offset_with_centering(self):
        obj = Text(
            ORIGIN,
            None,
            "testing",
            horizontal_alignment=HorizontalAlignment.CENTER,
            vertical_alignment=VerticalAlignment.CENTER,
        )
        offset = obj._alignment_offset
        # Generous epsilon is needed due to flaky font sizing
        assert_almost_equal(offset.x, Unit(-20), epsilon=2)
        assert_almost_equal(offset.y, Unit(2.5), epsilon=0.75)

    def test_alignment_offset_with_right_alignment(self):
        obj = Text(
            ORIGIN, None, "testing", horizontal_alignment=HorizontalAlignment.RIGHT
        )
        offset = obj._alignment_offset
        # Generous epsilon is needed due to flaky font sizing
        assert_almost_equal(offset.x, Unit(-40), epsilon=2)
        assert_almost_equal(offset.y, ZERO)

    def test_bounding_rect_with_scale(self):
        obj = Text(ORIGIN, None, "testing")
        unscaled_rect = obj.bounding_rect
        obj.scale = 2
        assert obj.bounding_rect == unscaled_rect * 2

    def test_bounding_rect_with_offset(self):
        obj = Text(ORIGIN, None, "testing")
        uncentered_rect = obj.bounding_rect
        obj.horizontal_alignment = HorizontalAlignment.CENTER
        obj.vertical_alignment = VerticalAlignment.CENTER
        centered_rect = obj.bounding_rect
        assert centered_rect.width == uncentered_rect.width
        assert centered_rect.height == uncentered_rect.height
        assert_almost_equal(centered_rect.x, Unit(-20), epsilon=2)
        assert_almost_equal(centered_rect.y, Unit(-5.5), epsilon=2)

    def test_rendered_interface_with_offset(self):
        obj = Text(
            ORIGIN,
            None,
            "testing",
            horizontal_alignment=HorizontalAlignment.CENTER,
            vertical_alignment=VerticalAlignment.CENTER,
        )
        obj._render()
        rendered_pos = obj.interfaces[0].pos
        assert_almost_equal(rendered_pos, Point(Unit(-20), Unit(2.5)), epsilon=1.5)
