import unittest

from brown.utils.color import Color
from brown.core.brush import Brush


class TestBrush(unittest.TestCase):

    def test_init_with_hex_color(self):
        test_pen = Brush('#eeddcc')
        assert(test_pen.color == Color(238, 221, 204, 255))

    def test_init_with_color_args_tuple(self):
        test_pen = Brush(('#eeddcc', 200))
        assert(test_pen.color == Color(238, 221, 204, 200))
