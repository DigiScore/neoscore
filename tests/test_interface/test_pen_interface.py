import unittest

from brown.utils.units import GraphicUnit, Mm
from brown.utils.color import Color
from brown.utils.stroke_pattern import StrokePattern
from brown.interface.pen_interface import PenInterface


class TestPenInterface(unittest.TestCase):

    def test_color_passed_to_qt(self):
        pen = PenInterface(Color(0, 100, 200, 250), Mm(1), StrokePattern(1))
        assert(pen._qt_object.color().red() == 0)
        assert(pen._qt_object.color().green() == 100)
        assert(pen._qt_object.color().blue() == 200)
        assert(pen._qt_object.color().alpha() == 250)

    def test_thickness_converted_to_qt_units(self):
        pen = PenInterface(Color("#ffffff"), Mm(1), StrokePattern(1))
        self.assertAlmostEqual(pen._qt_object.widthF(),
                               GraphicUnit(Mm(1)).value)

    def test_change_color_changes_qt_object(self):
        pen = PenInterface(Color("#ffffff"), Mm(1), StrokePattern(1))
        pen.color = Color(0, 100, 200, 250)
        assert(pen._qt_object.color().red() == 0)
        assert(pen._qt_object.color().green() == 100)
        assert(pen._qt_object.color().blue() == 200)
        assert(pen._qt_object.color().alpha() == 250)

    def test_change_thickness_changes_qt_object(self):
        pen = PenInterface(Color("#ffffff"), 0, StrokePattern(1))
        pen.thickness = Mm(1)
        self.assertAlmostEqual(pen._qt_object.widthF(),
                               GraphicUnit(Mm(1)).value)

    def test_change_stroke_pattern_changes_qt_object(self):
        pen = PenInterface(Color("#ffffff"), 0, StrokePattern(1))
        pen._qt_object.setStyle(2)
        assert(pen._qt_object.style() == 2)
