import unittest

from neoscore import constants
from neoscore.core.pen import Pen
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.interface.pen_interface import PenInterface
from neoscore.utils.color import Color
from neoscore.utils.units import Unit

from ..helpers import assert_almost_equal


class TestPen(unittest.TestCase):
    def test_init_with_hex_color(self):
        test_pen = Pen("#eeddcc")
        assert test_pen.color == Color(238, 221, 204, 255)

    def test_init_default_thicknes(self):
        test_pen = Pen("#eeddcc")
        assert_almost_equal(test_pen.thickness, constants.DEFAULT_PEN_THICKNESS)

    def test_init_default_pattern(self):
        test_pen = Pen()
        assert test_pen.pattern == PenPattern.SOLID

    def test_init_default_join_style(self):
        test_pen = Pen()
        assert test_pen.join_style == PenJoinStyle.BEVEL

    def test_init_default_cap_style(self):
        test_pen = Pen()
        assert test_pen.cap_style == PenCapStyle.SQUARE

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
        assert original.color == clone.color
        assert original.thickness == clone.thickness
        assert original.pattern == clone.pattern
        assert original.join_style == clone.join_style
        assert original.cap_style == clone.cap_style

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
