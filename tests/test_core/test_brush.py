import unittest

from neoscore.core.brush import Brush
from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.color import Color
from neoscore.interface.brush_interface import BrushInterface


class TestBrush(unittest.TestCase):
    def test_init_with_hex_color(self):
        brush = Brush("#eeddcc")
        assert brush.color == Color(238, 221, 204, 255)

    def test_pattern_defaults_to_solid_color(self):
        brush = Brush("#ffffff")
        assert brush.pattern == BrushPattern.SOLID

    def test_init_with_pattern(self):
        brush = Brush("#ffffff", BrushPattern.DENSE_1)
        assert brush.pattern == BrushPattern.DENSE_1

    def test_from_existing(self):
        original = Brush(Color("#ffffff"), BrushPattern.DENSE_1)
        clone = Brush.from_existing(original)
        assert id(original) != id(clone)
        assert original == clone
        assert Brush.from_existing(original, color="#000000").color == Color("#000000")
        assert (
            Brush.from_existing(original, pattern=BrushPattern.DENSE_2).pattern
            == BrushPattern.DENSE_2
        )

    def test_from_def(self):
        assert Brush.from_def(Brush("#ffffff")) == Brush("#ffffff")
        assert Brush.from_def("#ffffff") == Brush("#ffffff")

    def test_no_brush(self):
        brush = Brush.no_brush()
        assert brush == Brush(Brush._default_color, BrushPattern.INVISIBLE)
        assert id(brush) != Brush.no_brush()

    def test_interface_generation(self):
        brush = Brush(Color("#ffffff"), BrushPattern.DENSE_1)
        assert brush.interface == BrushInterface(Color("#ffffff"), BrushPattern.DENSE_1)

    def test_setters_update_interface(self):
        brush = Brush(Color("#000000"), BrushPattern.DENSE_1)
        brush.color = Color("#ffffff")
        assert brush.interface.color == Color("#ffffff")
        brush.pattern = BrushPattern.SOLID
        assert brush.interface.pattern == BrushPattern.SOLID

    def test__eq__(self):
        brush = Brush(Color("#000000"), BrushPattern.DENSE_1)
        assert brush == Brush.from_existing(brush)
        assert brush != "some other type object"
        assert brush != Brush.from_existing(brush, color="#ffffff")
        assert brush != Brush.from_existing(brush, pattern=BrushPattern.SOLID)
