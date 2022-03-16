import unittest

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.core.invisible_object import InvisibleObject
from neoscore.core.text import Text
from neoscore.utils.units import ZERO, Unit


class TestText(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.font = Font("Bravura", 12, 1, False)

    def test_init(self):
        mock_parent = InvisibleObject((Unit(10), Unit(11)), parent=None)
        obj = Text((Unit(5), Unit(6)), mock_parent, "testing", self.font)
        assert obj.x == Unit(5)
        assert obj.y == Unit(6)
        assert obj.text == "testing"
        assert obj.font == self.font
        assert obj.parent == mock_parent

    def test_default_init_values(self):
        obj = Text((Unit(5), Unit(6)), None, "testing")
        assert obj.font == neoscore.default_font
        assert obj.parent == neoscore.document.pages[0]

    def test_length_when_non_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=False)
        assert obj.length == ZERO

    def test_length_when_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        # Can't assert exact length since this can flake
        assert obj.length == obj.bounding_rect.width

    def test_breakable_setter(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        assert obj.length == obj.bounding_rect.width
        obj.breakable = False
        assert obj.length == ZERO
