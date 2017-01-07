import unittest

from brown.core import brown
from brown.utils.color import Color
from brown.core.brush import Brush


class TestBrush(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init_with_hex_color(self):
        test_brush = Brush('#eeddcc')
        assert(test_brush.color == Color(238, 221, 204, 255))

    def test_init_with_color_args_tuple(self):
        test_brush = Brush(('#eeddcc', 200))
        assert(test_brush.color == Color(238, 221, 204, 200))
