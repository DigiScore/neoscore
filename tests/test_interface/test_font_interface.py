from neoscore.core import neoscore
from neoscore.core.units import Unit
from neoscore.interface.font_interface import FontInterface

from ..helpers import AppTest


class MockUnit(Unit):
    CONVERSION_RATE = 0.5


class TestFontInterface(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.app_interface._remove_all_loaded_fonts()

    def test_init(self):
        test_font = FontInterface("Bravura", MockUnit(12), 1, False)
        assert test_font.family_name == "Bravura"
        assert test_font.size == MockUnit(12)
        assert test_font.weight == 1
        assert test_font.italic is False
        assert test_font.qt_object.bold() is False
        assert test_font.qt_object.italic() is False
        assert test_font.qt_object.pixelSize() == 6
        assert test_font.qt_object.weight() == 1
        # These values seem to flakily vary between runs
        # assert test_font.ascent == MockUnit(18)
        # assert test_font.descent == MockUnit(6)
        # assert test_font.x_height == MockUnit(10)

    def test_float_point_sizes(self):
        test_font = FontInterface("Bravura", MockUnit(13), 1, False)
        self.assertAlmostEqual(test_font.qt_object.pixelSize(), 6)
