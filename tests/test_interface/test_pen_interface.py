import unittest

from neoscore.core.color import Color
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Mm
from neoscore.interface.pen_interface import PenInterface


class TestPenInterface(unittest.TestCase):
    def test_qt_object_creation(self):
        pen = PenInterface(
            Color(0, 100, 200, 250),
            Mm(1),
            PenPattern.SOLID,
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        assert pen.qt_object.color().red() == 0
        assert pen.qt_object.color().green() == 100
        assert pen.qt_object.color().blue() == 200
        assert pen.qt_object.color().alpha() == 250
        self.assertAlmostEqual(pen.qt_object.widthF(), Mm(1).base_value)
        assert pen.qt_object.style() == PenPattern.SOLID.value
        assert pen.qt_object.joinStyle() == PenJoinStyle.BEVEL.value
        assert pen.qt_object.capStyle() == PenCapStyle.SQUARE.value
