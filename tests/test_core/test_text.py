from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.font import Font
from neoscore.core.pen import Pen
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.text import Text
from neoscore.utils.units import ZERO, Unit

from ..helpers import AppTest


class TestText(AppTest):
    def setUp(self):
        super().setUp()
        self.font = Font("Bravura", 12, 1, False)

    def test_init(self):
        pen = Pen("#00ff00")
        brush = Brush("#ff0000")
        mock_parent = PositionedObject((Unit(10), Unit(11)), None)
        obj = Text(
            (Unit(5), Unit(6)), mock_parent, "testing", self.font, brush, pen, 2, False
        )
        assert obj.x == Unit(5)
        assert obj.y == Unit(6)
        assert obj.text == "testing"
        assert obj.font == self.font
        assert obj.parent == mock_parent
        assert obj.brush == brush
        assert obj.pen == pen

    def test_default_init_values(self):
        obj = Text((Unit(5), Unit(6)), None, "testing")
        assert obj.font == neoscore.default_font
        assert obj.parent == neoscore.document.pages[0]
        assert obj.brush == Brush()
        assert obj.pen == Pen.no_pen()
        assert obj.scale == 1
        assert obj.breakable == True

    def test_length_when_non_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=False)
        assert obj.breakable_length == ZERO

    def test_length_when_breakable(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        # Can't assert exact length since this can flake
        assert obj.breakable_length == obj.bounding_rect.width

    def test_breakable_setter(self):
        obj = Text((Unit(5), Unit(6)), None, "testing", breakable=True)
        assert obj.breakable_length == obj.bounding_rect.width
        obj.breakable = False
        assert obj.breakable_length == ZERO
