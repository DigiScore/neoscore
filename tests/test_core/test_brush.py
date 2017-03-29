import unittest

from brown.core import brown
from brown.core.fill_pattern import FillPattern
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

    def test_pattern_defaults_to_solid_color(self):
        test_brush = Brush('#ffffff')
        assert(test_brush.pattern == FillPattern.SOLID)

    def test_pattern_set_from_real_pattern_object(self):
        test_brush = Brush('#ffffff', FillPattern.DENSE_1)
        assert(test_brush.pattern == FillPattern.DENSE_1)

    def test_pattern_set_from_int_enum_value(self):
        test_brush = Brush('#ffffff', FillPattern.DENSE_1.value)
        assert(test_brush.pattern == FillPattern.DENSE_1)

    def test_from_existing(self):
        original = Brush(Color('#ffffff'), FillPattern.DENSE_1.value)
        clone = Brush.from_existing(original)
        assert(id(original) != id(clone))
        assert(original.color == clone.color)
        assert(original.pattern == clone.pattern)
