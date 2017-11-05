import unittest

from brown.core.pen_pattern import PenPattern
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.units import GraphicUnit, Mm


class TestPenInterface(unittest.TestCase):

    def test_color_passed_to_qt(self):
        pen = PenInterface(None, Color(0, 100, 200, 250), Mm(1), PenPattern(1))
        assert(pen.qt_object.color().red() == 0)
        assert(pen.qt_object.color().green() == 100)
        assert(pen.qt_object.color().blue() == 200)
        assert(pen.qt_object.color().alpha() == 250)

    def test_thickness_converted_to_qt_units(self):
        pen = PenInterface(None, Color("#ffffff"), Mm(1), PenPattern(1))
        self.assertAlmostEqual(pen.qt_object.widthF(),
                               GraphicUnit(Mm(1)).value)

    def test_change_color_changesqt_object(self):
        pen = PenInterface(None, Color("#ffffff"), Mm(1), PenPattern(1))
        pen.color = Color(0, 100, 200, 250)
        assert(pen.qt_object.color().red() == 0)
        assert(pen.qt_object.color().green() == 100)
        assert(pen.qt_object.color().blue() == 200)
        assert(pen.qt_object.color().alpha() == 250)

    def test_change_thickness_changesqt_object(self):
        pen = PenInterface(None, Color("#ffffff"), 0, PenPattern(1))
        pen.thickness = Mm(1)
        self.assertAlmostEqual(pen.qt_object.widthF(),
                               GraphicUnit(Mm(1)).value)

    def test_change_pen_pattern_changesqt_object(self):
        pen = PenInterface(None, Color("#ffffff"), 0, PenPattern(1))
        pen.qt_object.setStyle(2)
        assert(pen.qt_object.style() == 2)
