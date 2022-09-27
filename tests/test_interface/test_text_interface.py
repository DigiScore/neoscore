from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.color import Color
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Unit
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.text_interface import TextInterface

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
            "foo",
            self.font,
        )
        test_font_2 = FontInterface("Bravura", Unit(24), 1, False)
        test_object_2 = TextInterface(
            ORIGIN,
            self.brush,
            self.pen,
            "foo",
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
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font)
        assert text._create_qt_object().scale() == 1
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font, scale=2)
        assert text._create_qt_object().scale() == 2

    def test_rotation(self):
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font)
        assert text._create_qt_object().rotation() == 0
        text = TextInterface(
            ORIGIN, self.brush, self.pen, "foo", self.font, rotation=123
        )
        assert text._create_qt_object().rotation() == 123

    def test_transformOriginPoint(self):
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font)
        assert text._create_qt_object().transformOriginPoint() == point_to_qt_point_f(
            ORIGIN
        )
        text = TextInterface(
            ORIGIN,
            self.brush,
            self.pen,
            "foo",
            self.font,
            transform_origin=Point(Unit(12), Unit(12)),
        )
        # assert text._create_qt_object().transformOriginPoint() == point_to_qt_point_f(Point(Unit(12),Unit(12)))

    def test_z_index(self):
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font)
        assert text._create_qt_object().zValue() == 0
        text = TextInterface(ORIGIN, self.brush, self.pen, "foo", self.font, z_index=99)
        assert text._create_qt_object().zValue() == 99
