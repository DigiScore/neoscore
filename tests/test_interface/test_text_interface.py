from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.pen import Pen
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.text_interface import TextInterface
from neoscore.utils.color import Color
from neoscore.utils.point import ORIGIN
from neoscore.utils.units import Unit

from ..helpers import AppTest


class TestTextInterface(AppTest):
    def setUp(self):
        super().setUp()
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)
        self.pen = Pen.no_pen().interface
        self.font = FontInterface("Bravura", Unit(12), 1, False)

    def test_path_caching(self):
        test_object_1 = TextInterface(
            ORIGIN,
            self.brush,
            self.pen,
            "testing",
            self.font,
        )
        test_font_2 = FontInterface("Bravura", Unit(24), 1, False)
        test_object_2 = TextInterface(
            ORIGIN,
            self.brush,
            self.pen,
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

    def test_scale(self):
        assert (
            TextInterface(ORIGIN, self.brush, self.pen, "testing", self.font)
            ._create_qt_object()
            .scale()
            == 1
        )
        assert (
            TextInterface(ORIGIN, self.brush, self.pen, "testing", self.font, scale=2)
            ._create_qt_object()
            .scale()
            == 2
        )

    def test_rotation(self):
        assert (
            TextInterface(ORIGIN, self.brush, self.pen, "testing", self.font)
            ._create_qt_object()
            .rotation()
            == 0
        )
        assert (
            TextInterface(
                ORIGIN, self.brush, self.pen, "testing", self.font, rotation=123
            )
            ._create_qt_object()
            .rotation()
            == 123
        )
