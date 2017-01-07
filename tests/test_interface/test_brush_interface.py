import unittest

from brown.interface.brush_interface import BrushInterface
from brown.utils.color import Color


class TestBrushInterface(unittest.TestCase):

    def test_color_passed_to_qt(self):
        brush = BrushInterface(Color(0, 100, 200, 250))
        assert(brush._qt_object.color().red() == 0)
        assert(brush._qt_object.color().green() == 100)
        assert(brush._qt_object.color().blue() == 200)
        assert(brush._qt_object.color().alpha() == 250)
