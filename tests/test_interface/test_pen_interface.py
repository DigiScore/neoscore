import unittest

from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.units import GraphicUnit, Mm


class TestPenInterface(unittest.TestCase):
    def test_color_passed_to_qt(self):
        pen = PenInterface(
            Color(0, 100, 200, 250),
            Mm(1),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        assert pen.qt_object.color().red() == 0
        assert pen.qt_object.color().green() == 100
        assert pen.qt_object.color().blue() == 200
        assert pen.qt_object.color().alpha() == 250

    def test_thickness_converted_to_qt_units(self):
        pen = PenInterface(
            Color("#ffffff"),
            Mm(1),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        self.assertAlmostEqual(pen.qt_object.widthF(), GraphicUnit(Mm(1)).value)

    def test_change_color_propagated_to_qt_object(self):
        pen = PenInterface(
            Color("#ffffff"),
            Mm(1),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        pen.color = Color(0, 100, 200, 250)
        assert pen.qt_object.color().red() == 0
        assert pen.qt_object.color().green() == 100
        assert pen.qt_object.color().blue() == 200
        assert pen.qt_object.color().alpha() == 250

    def test_change_thickness_propagated_to_qt_object(self):
        pen = PenInterface(
            Color("#ffffff"),
            0,
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        pen.thickness = Mm(1)
        self.assertAlmostEqual(pen.qt_object.widthF(), GraphicUnit(Mm(1)).value)

    def test_change_pen_pattern_propagated_to_qt_object(self):
        pen = PenInterface(
            Color("#ffffff"),
            0,
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        pen.pattern = PenPattern.DASHDOTDOT
        assert pen.qt_object.style() == PenPattern.DASHDOTDOT.value

    def test_change_join_style_propagated_to_qt_object(self):
        pen = PenInterface(
            Color("#ffffff"),
            Mm(1),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        pen.join_style = PenJoinStyle.MITER
        assert pen.qt_object.joinStyle() == PenJoinStyle.MITER.value

    def test_change_cap_style_propagated_to_qt_object(self):
        pen = PenInterface(
            Color("#ffffff"),
            Mm(1),
            PenPattern(1),
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        pen.cap_style = PenCapStyle.ROUND
        assert pen.qt_object.capStyle() == PenCapStyle.ROUND.value
