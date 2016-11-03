import unittest

from brown.core.pen import Pen


class TestPen(unittest.TestCase):

    def test_init(self):
        test_pen = Pen('#ffffff')
        assert(test_pen.color == '#ffffff')

    def test_default_color(self):
        # Default value API change canary
        test_pen = Pen()
        assert(test_pen.color == '#000000')

    def test_color_setter_changes_interface(self):
        test_pen = Pen()
        test_pen.color = '#eeeeee'
        assert(test_pen.color == '#eeeeee')
        assert(test_pen._interface.color == '#eeeeee')
