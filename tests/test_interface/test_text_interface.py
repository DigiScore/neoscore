import unittest

from brown.core import brown
from brown.core.brush_pattern import BrushPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.font_interface import FontInterface
from brown.interface.text_interface import TextInterface
from brown.utils.color import Color


class TestTextInterface(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.brush = BrushInterface(None, Color("#000000"), BrushPattern.SOLID)

    def test_init(self):
        test_font = FontInterface(None, "Bravura", 12, 1, False)
        test_object = TextInterface(None, (5, 6), "testing", test_font, self.brush)
        assert test_object.text == "testing"
        assert test_object.qt_object.text() == test_object.text
        assert test_object.font == test_font
        assert test_object.qt_object.font() == test_object.font.qt_object

    def test_text_setter_changesqt_object(self):
        test_font = FontInterface(None, "Bravura", 12, 1, False)
        test_object = TextInterface(None, (5, 6), "testing", test_font, self.brush)
        test_object.text = "new value"
        assert test_object.text == "new value"
        assert test_object.qt_object.text() == "new value"

    def test_font_setter_changesqt_object(self):
        test_font = FontInterface(None, "Bravura", 12, 1, False)
        test_object = TextInterface(None, (5, 6), "testing", test_font, self.brush)
        new_test_font = FontInterface(None, "Bravura", 16, 1, False)
        test_object.font = new_test_font
        assert test_object.font == new_test_font
        assert test_object.qt_object.font() == new_test_font.qt_object
