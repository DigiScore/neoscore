import unittest

from neoscore.core.color import Color
from neoscore.core.pen import Pen
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import ZERO, Unit
from neoscore.interface.pen_interface import PenInterface

from ..helpers import assert_almost_equal


class TestPen(unittest.TestCase):
    def test_init_with_hex_color(self):
        test_pen = Pen("#eeddcc")
        assert test_pen.color == Color(238, 221, 204, 255)

    def test_init_default_thicknes(self):
        test_pen = Pen("#eeddcc")
        assert_almost_equal(test_pen.thickness, ZERO)

    def test_init_default_pattern(self):
        test_pen = Pen()
        assert test_pen.pattern == PenPattern.SOLID

    def test_init_default_join_style(self):
        test_pen = Pen()
        assert test_pen.join_style == PenJoinStyle.MITER

    def test_init_default_cap_style(self):
        test_pen = Pen()
        assert test_pen.cap_style == PenCapStyle.FLAT

    def test_from_existing(self):
        original = Pen(
            Color("#eeddcc"),
            Unit(2),
            PenPattern.DASH,
            PenJoinStyle.MITER,
            PenCapStyle.ROUND,
        )
        clone = Pen.from_existing(original)
        assert id(original) != id(clone)
        assert original == clone
        assert Pen.from_existing(original, color="#ffffff").color == Color("#ffffff")
        assert Pen.from_existing(original, thickness=Unit(1)).thickness == Unit(1)
        assert (
            Pen.from_existing(original, pattern=PenPattern.SOLID).pattern
            == PenPattern.SOLID
        )
        assert (
            Pen.from_existing(original, join_style=PenJoinStyle.BEVEL).join_style
            == PenJoinStyle.BEVEL
        )
        assert (
            Pen.from_existing(original, cap_style=PenCapStyle.FLAT).cap_style
            == PenCapStyle.FLAT
        )

    def test_from_def(self):
        assert Pen.from_def(Pen("#ffffff")) == Pen("#ffffff")
        assert Pen.from_def("#ffffff") == Pen("#ffffff")

    def test_no_pen(self):
        pen = Pen.no_pen()
        assert pen == Pen(pattern=PenPattern.INVISIBLE)
        assert id(pen) != id(Pen.no_pen())

    def test_interface_generation(self):
        pen = Pen(
            Color("#eeddcc"),
            Unit(2),
            PenPattern.DASH,
            PenJoinStyle.MITER,
            PenCapStyle.ROUND,
        )
        assert pen.interface == PenInterface(
            Color("#eeddcc"),
            Unit(2),
            PenPattern.DASH,
            PenJoinStyle.MITER,
            PenCapStyle.ROUND,
        )

    def test_color_setter_with_hex_string(self):
        pen = Pen("#ff0000")
        pen.color = "#00ff00"
        assert pen.color == Color("#00ff00")

    def test_setters_update_interface(self):
        pen = Pen(
            Color("#eeddcc"),
            Unit(2),
            PenPattern.DASH,
            PenJoinStyle.MITER,
            PenCapStyle.ROUND,
        )
        pen.color = Color("#ffffff")
        assert pen.interface.color == Color("#ffffff")
        pen.thickness = Unit(1)
        assert pen.interface.thickness == Unit(1)
        pen.pattern = PenPattern.SOLID
        assert pen.interface.pattern == PenPattern.SOLID
        pen.join_style = PenJoinStyle.MITER
        assert pen.interface.join_style == PenJoinStyle.MITER
        pen.cap_style = PenCapStyle.ROUND
        assert pen.interface.cap_style == PenCapStyle.ROUND

    def test__eq__(self):
        original = Pen(
            Color("#eeddcc"),
            Unit(2),
            PenPattern.DASH,
            PenJoinStyle.MITER,
            PenCapStyle.ROUND,
        )
        assert Pen.from_existing(original) == original
        assert original != "some other type object"
        assert Pen.from_existing(original, color="#ffffff") != original
        assert Pen.from_existing(original, thickness=Unit(1)) != original
        assert Pen.from_existing(original, pattern=PenPattern.SOLID) != original
        assert Pen.from_existing(original, join_style=PenJoinStyle.BEVEL) != original
        assert Pen.from_existing(original, cap_style=PenCapStyle.FLAT) != original
