import unittest

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.interface import text_interface
from brown.interface.brush_interface import BrushInterface
from brown.interface.font_interface import FontInterface
from brown.interface.pen_interface import NO_PEN
from brown.interface.text_interface import TextInterface
from brown.utils.color import Color
from brown.utils.point import Point
from brown.utils.units import Unit


class TestTextInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_path_caching(self):
        test_font_1 = FontInterface("Bravura", Unit(12), 1, False)
        test_object_1 = TextInterface(
            Point(Unit(5), Unit(6)),
            NO_PEN,
            self.brush,
            "testing",
            test_font_1,
        )
        test_font_2 = FontInterface("Bravura", Unit(24), 1, False)
        test_object_2 = TextInterface(
            Point(Unit(5), Unit(6)),
            NO_PEN,
            self.brush,
            "testing",
            test_font_2,
        )
        # Since the fonts and texts matched, the underlying paths
        # should be equal by reference.
        test_qt_object_1 = test_object_1._create_qt_object()
        test_qt_object_2 = test_object_2._create_qt_object()
        assert test_qt_object_1.path() == test_qt_object_2.path()
        assert test_qt_object_1.scale() == 1
        assert test_qt_object_2.scale() == 2
