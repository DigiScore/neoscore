import unittest

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.interface import text_interface
from brown.interface.brush_interface import BrushInterface
from brown.interface.font_interface import FontInterface
from brown.interface.text_interface import TextInterface
from brown.utils.color import Color


class TestTextInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_path_caching(self):
        test_font_1 = FontInterface("Bravura", 12, 1, False)
        test_object_1 = TextInterface((5, 6), "testing", test_font_1, self.brush)
        test_font_2 = FontInterface("Bravura", 24, 1, False)
        test_object_2 = TextInterface((5, 6), "testing", test_font_2, self.brush)
        # Since the fonts and texts matched, the underlying paths
        # should be equal by reference.
        assert test_object_1.qt_object.path() == test_object_2.qt_object.path()
        assert test_object_1.qt_object.scale() == 1
        assert test_object_2.qt_object.scale() == 2
