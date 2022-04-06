from neoscore.core import neoscore
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Unit
from neoscore.interface.rich_text_interface import RichTextInterface

from ..helpers import AppTest


class TestRichTextInterface(AppTest):
    def setUp(self):
        super().setUp()
        self.font = neoscore.default_font.interface
        self.html = "<p>test</p>"

    def test_qt_object_properties(self):
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)), self.html, self.font, Unit(50), 2, 15, 99
        )
        qt_object = interface._create_qt_object()
        assert qt_object.document().toPlainText() == "test"
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.textWidth() == 50
        assert qt_object.rotation() == 15
        assert qt_object.font() == self.font.qt_object
        assert qt_object.zValue() == 99

    def test_automatic_text_width(self):
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)), self.html, self.font, None
        )
        qt_object = interface._create_qt_object()
        assert qt_object.textWidth() == -1

    def test_scale(self):
        text = RichTextInterface(ORIGIN, self.html, self.font)
        assert text._create_qt_object().scale() == 1
        text = RichTextInterface(ORIGIN, self.html, self.font, scale=2)
        assert text._create_qt_object().scale() == 2

    def test_rotation(self):
        text = RichTextInterface(ORIGIN, self.html, self.font)
        assert text._create_qt_object().rotation() == 0
        text = RichTextInterface(ORIGIN, self.html, self.font, rotation=123)
        assert text._create_qt_object().rotation() == 123

    def test_z_index(self):
        text = RichTextInterface(ORIGIN, self.html, self.font)
        assert text._create_qt_object().zValue() == 0
        text = RichTextInterface(ORIGIN, self.html, self.font, z_index=99)
        assert text._create_qt_object().zValue() == 99
