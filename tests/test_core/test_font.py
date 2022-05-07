import pytest

from neoscore.core.font import Font
from neoscore.core.rect import Rect
from neoscore.core.units import Unit

from ..helpers import AppTest


class TestFont(AppTest):
    def test_init(self):
        test_font = Font("Bravura", 12, 2, False)
        assert test_font.family_name == "Bravura"
        assert test_font.size == Unit(12)
        assert test_font.weight == 2
        assert test_font.italic is False
        assert test_font.interface.family_name == "Bravura"
        assert test_font.interface.size == Unit(12)
        assert test_font.interface.weight == 2
        assert test_font.interface.italic is False

    def test_default_init_values(self):
        # API default values canary
        test_font = Font("Bravura", 12)
        assert test_font.weight is None
        assert test_font.italic is False

    def test_modified(self):
        test_font = Font("Bravura", 12, 2, False)
        modifying_family_name = test_font.modified(size=14, weight=1, italic=True)
        assert modifying_family_name.family_name == "Bravura"
        assert modifying_family_name.size == Unit(14)
        assert modifying_family_name.weight == 1
        assert modifying_family_name.italic is True

        modifying_size = test_font.modified(
            family_name="Cormorant Garamond", weight=1, italic=True
        )
        assert modifying_size.family_name == "Cormorant Garamond"
        assert modifying_size.size == Unit(12)
        assert modifying_size.weight == 1
        assert modifying_size.italic is True

        modifying_weight = test_font.modified(
            family_name="Cormorant Garamond", size=14, italic=True
        )
        assert modifying_weight.family_name == "Cormorant Garamond"
        assert modifying_weight.size == Unit(14)
        assert modifying_weight.weight == 2
        assert modifying_weight.italic is True

        modifying_italic = test_font.modified(
            family_name="Cormorant Garamond", size=14, weight=2
        )
        assert modifying_italic.family_name == "Cormorant Garamond"
        assert modifying_italic.size == Unit(14)
        assert modifying_italic.weight == 2
        assert modifying_italic.italic is False

    def test__str__(self):
        font = Font("Bravura", 12, 1, False)
        assert str(font) == "Font('Bravura', Unit(12), 1, False)"

    def test__eq__(self):
        font = Font("Bravura", 12, 1, False)
        assert font == Font("Bravura", 12, 1, False)
        assert font != Font("Cormorant Garamond", 12, 1, False)
        assert font != Font("Bravura", 13, 1, False)
        assert font != Font("Bravura", 12, 2, False)
        assert font != Font("Bravura", 12, 1, True)

    def test__hash__(self):
        font = Font("Bravura", 12, 1, False)
        assert hash(font) == hash(Font("Bravura", 12, 1, False))
        assert hash(font) != hash(Font("Cormorant Garamond", 12, 1, False))
        assert hash(font) != hash(Font("Bravura", 13, 1, False))
        assert hash(font) != hash(Font("Bravura", 12, 2, False))
        assert hash(font) != hash(Font("Bravura", 12, 1, True))

    @pytest.mark.skip(reason="Exact loaded Qt font size seems to flake")
    def test_bounding_rect_of(self):
        font = Font("Bravura", 12, 1, False)
        rect = font.bounding_rect_of("")
        assert rect == Rect(Unit(0), Unit(0), Unit(0), Unit(0))
        rect = font.bounding_rect_of("abc")
        assert rect == Rect(Unit(1), Unit(-14), Unit(29), Unit(14))
