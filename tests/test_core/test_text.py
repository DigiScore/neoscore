import unittest

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.core.invisible_object import InvisibleObject
from neoscore.core.text import Text
from neoscore.utils.units import GraphicUnit, Unit


class TestText(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.font = Font("Bravura", 12, 1, False)

    def test_init(self):
        mock_parent = InvisibleObject((Unit(10), Unit(11)), parent=None)
        test_object = Text((Unit(5), Unit(6)), "testing", self.font, mock_parent)
        assert test_object.x == GraphicUnit(5)
        assert test_object.y == GraphicUnit(6)
        assert test_object.text == "testing"
        assert test_object.font == self.font
        assert test_object.parent == mock_parent

    def test_default_init_values(self):
        test_object = Text((Unit(5), Unit(6)), "testing")
        assert test_object.font == neoscore.default_font
        assert test_object.parent == neoscore.document.pages[0]
