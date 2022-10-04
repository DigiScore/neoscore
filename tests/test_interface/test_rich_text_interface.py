from neoscore.core import neoscore
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Unit
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.rich_text_interface import RichTextInterface

from ..helpers import AppTest


class TestRichTextInterface(AppTest):
    def setUp(self):
        super().setUp()
        self.font = neoscore.default_font.interface
        self.html = "<p>test</p>"

    def test_qt_object_properties(self):
        transform_origin = Point(Unit(12), Unit(12))
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)),
            None,
            2,
            15,
            transform_origin,
            self.html,
            self.font,
            Unit(50),
        )
        qt_object = interface._create_qt_object()
        assert qt_object.document().toPlainText() == "test"
        assert qt_object.document().documentMargin() == 0
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.textWidth() == 50
        assert qt_object.rotation() == 15
        assert qt_object.font() == self.font.qt_object
        assert qt_object.transformOriginPoint() == point_to_qt_point_f(transform_origin)

    def test_automatic_text_width(self):
        interface = RichTextInterface(
            Point(Unit(5), Unit(6)), None, 1, 0, ORIGIN, self.html, self.font
        )
        qt_object = interface._create_qt_object()
        assert qt_object.textWidth() == -1
