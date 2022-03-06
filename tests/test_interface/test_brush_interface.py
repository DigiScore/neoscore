import unittest

from brown.core.brush_pattern import BrushPattern
from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class TestBrushInterface(unittest.TestCase):
    def test_qt_object_creation(self):
        brush = BrushInterface(Color(0, 100, 200, 250), BrushPattern.SOLID)
        assert brush.qt_object.color().red() == 0
        assert brush.qt_object.color().green() == 100
        assert brush.qt_object.color().blue() == 200
        assert brush.qt_object.color().alpha() == 250
        assert brush.qt_object.style() == BrushPattern.SOLID.value
