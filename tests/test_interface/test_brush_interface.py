import unittest

from brown.core.brush_pattern import BrushPattern
from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class TestBrushInterface(unittest.TestCase):

    def test_color_passed_to_qt(self):
        brush = BrushInterface(Color(0, 100, 200, 250),
                               BrushPattern.SOLID)
        assert(brush._qt_object.color().red() == 0)
        assert(brush._qt_object.color().green() == 100)
        assert(brush._qt_object.color().blue() == 200)
        assert(brush._qt_object.color().alpha() == 250)

    def test_brush_pattern_passed_to_qt(self):
        brush = BrushInterface(Color(0, 0, 0),
                               BrushPattern.SOLID)
        assert(brush._qt_object.style() == BrushPattern.SOLID.value)

        brush = BrushInterface(Color(0, 0, 0),
                               BrushPattern.DENSE_1)
        assert(brush._qt_object.style() == BrushPattern.DENSE_1.value)
