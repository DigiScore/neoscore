import unittest

from brown.core import brown
from brown.core.font import Font
from brown.utils.units import GraphicUnit


class TestFont(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        test_font = Font("Bravura", 12, 2, False)
        assert test_font.family_name == "Bravura"
        assert test_font.size == GraphicUnit(12)
        assert test_font.weight == 2
        assert test_font.italic is False
        assert test_font._interface.family_name == "Bravura"
        assert test_font._interface.size == GraphicUnit(12)
        assert test_font._interface.weight == 2
        assert test_font._interface.italic is False

    def test_default_init_values(self):
        # API default values canary
        test_font = Font("Bravura", 12)
        assert test_font.weight is None
        assert test_font.italic is False

    def test_modified(self):
        test_font = Font("Bravura", 12, 2, False)
        modifying_family_name = test_font.modified(size=14, weight=1, italic=True)
        assert modifying_family_name.family_name == "Bravura"
        assert modifying_family_name.size == GraphicUnit(14)
        assert modifying_family_name.weight == 1
        assert modifying_family_name.italic is True

        modifying_size = test_font.modified(
            family_name="Cormorant Garamond", weight=1, italic=True
        )
        assert modifying_size.family_name == "Cormorant Garamond"
        assert modifying_size.size == GraphicUnit(12)
        assert modifying_size.weight == 1
        assert modifying_size.italic is True

        modifying_weight = test_font.modified(
            family_name="Cormorant Garamond", size=14, italic=True
        )
        assert modifying_weight.family_name == "Cormorant Garamond"
        assert modifying_weight.size == GraphicUnit(14)
        assert modifying_weight.weight == 2
        assert modifying_weight.italic is True

        modifying_italic = test_font.modified(
            family_name="Cormorant Garamond", size=14, weight=2
        )
        assert modifying_italic.family_name == "Cormorant Garamond"
        assert modifying_italic.size == GraphicUnit(14)
        assert modifying_italic.weight == 2
        assert modifying_italic.italic is False
