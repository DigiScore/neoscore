from neoscore.core import neoscore
from neoscore.interface.rich_text_interface import RichTextInterface
from neoscore.utils.point import Point
from neoscore.utils.units import Unit

from ..helpers import AppTest


class TestRichTextInterface(AppTest):
    def setUp(self):
        super().setUp()
        self.font = neoscore.default_font.interface
        self.html = "<p>test</p>"

    def test_qt_object_properties(self):
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)), self.html, self.font, Unit(50), 2, 15
        )
        qt_object = interface._create_qt_object()
        assert qt_object.document().toPlainText() == "test"
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.textWidth() == 50
        assert qt_object.rotation() == 15
        assert qt_object.font() == self.font.qt_object

    def test_automatic_text_width(self):
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)), self.html, self.font, None
        )
        qt_object = interface._create_qt_object()
        assert qt_object.textWidth() == -1
