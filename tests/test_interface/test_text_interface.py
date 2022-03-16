import unittest

from neoscore.core import neoscore
from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.pen import NO_PEN
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.text_interface import TextInterface
from neoscore.utils.color import Color
from neoscore.utils.point import Point
from neoscore.utils.units import Unit


class TestTextInterface(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_path_caching(self):
        test_font_1 = FontInterface("Bravura", Unit(12), 1, False)
        test_object_1 = TextInterface(
            Point(Unit(5), Unit(6)),
            self.brush,
            NO_PEN.interface,
            "testing",
            test_font_1,
        )
        test_font_2 = FontInterface("Bravura", Unit(24), 1, False)
        test_object_2 = TextInterface(
            Point(Unit(5), Unit(6)),
            self.brush,
            NO_PEN.interface,
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
