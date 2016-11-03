import unittest

from brown.core.brush import Brush


class TestBrush(unittest.TestCase):

    def test_init(self):
        test_brush = Brush('#ffffff')
        assert(test_brush.color == '#ffffff')

    def test_default_color(self):
        # Default value API change canary
        test_brush = Brush()
        assert(test_brush.color == '#000000')

    def test_color_setter_changes_interface(self):
        test_brush = Brush()
        test_brush.color = '#eeeeee'
        assert(test_brush.color == '#eeeeee')
        assert(test_brush._interface.color == '#eeeeee')
