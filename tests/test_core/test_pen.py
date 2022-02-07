import unittest

from brown import constants
from brown.core import brown
from brown.core.pen import Pen
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.utils.color import Color
from brown.utils.units import Unit


class TestPen(unittest.TestCase):
    def test_init_with_hex_color(self):
        test_pen = Pen("#eeddcc")
        assert test_pen.color == Color(238, 221, 204, 255)

    def test_init_with_color_args_tuple(self):
        test_pen = Pen(("#eeddcc", 200))
        assert test_pen.color == Color(238, 221, 204, 200)

    def test_init_default_thicknes(self):
        test_pen = Pen(("#eeddcc", 200))
        self.assertAlmostEqual(
            Unit(test_pen.thickness).value, Unit(constants.DEFAULT_PEN_THICKNESS).value
        )

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
