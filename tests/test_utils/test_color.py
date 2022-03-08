import unittest

import pytest

from brown.utils.color import Color, ColorBoundsError, color_from_def


class TestColor(unittest.TestCase):
    def test_init_with_hex_string(self):
        color = Color("eeddcc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_hex_string_with_leading_pound(self):
        color = Color("#eeddcc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_rgb(self):
        color = Color(0, 100, 200)
        assert color.red == 0
        assert color.green == 100
        assert color.blue == 200
        assert color.alpha == 255

    def test_init_with_rgba(self):
        color = Color(0, 100, 200, 250)
        assert color.red == 0
        assert color.green == 100
        assert color.blue == 200
        assert color.alpha == 250

    def test_bad_red_color_value(self):
        with pytest.raises(ColorBoundsError):
            Color(256, 0, 0, 0)
        with pytest.raises(ColorBoundsError):
            Color(-1, 0, 0, 0)

    def test_bad_green_color_value(self):
        with pytest.raises(ColorBoundsError):
            Color(0, 256, 0, 0)
        with pytest.raises(ColorBoundsError):
            Color(0, -1, 0, 0)

    def test_bad_blue_color_value(self):
        with pytest.raises(ColorBoundsError):
            Color(0, 0, 256, 0)
        with pytest.raises(ColorBoundsError):
            Color(0, 0, -1, 0)

    def test_bad_alpha_color_value(self):
        with pytest.raises(ColorBoundsError):
            Color(0, 0, 0, 256)
        with pytest.raises(ColorBoundsError):
            Color(0, 0, 0, -1)

    def test__repr__(self):
        color = Color(0, 100, 200, 250)
        assert color.__repr__() == "Color(0, 100, 200, 250)"

    def test__eq__(self):
        assert Color(0, 100, 200, 250) == Color(0, 100, 200, 250)

    def test__ne__(self):
        assert Color(1, 100, 200, 250) != Color(0, 100, 200, 250)
        assert Color(0, 101, 200, 250) != Color(0, 100, 200, 250)
        assert Color(0, 100, 201, 250) != Color(0, 100, 200, 250)
        assert Color(0, 100, 200, 251) != Color(0, 100, 200, 250)
        assert Color(0, 100, 200, 250) != "nonsense"

    def test__hash__(self):
        assert {
            Color(0, 100, 200, 250),
            Color(0, 100, 200, 250),
            Color(0, 0, 0, 0),
        } == {Color(0, 100, 200, 250), Color(0, 0, 0, 0)}

    def test_color_from_def(self):
        assert color_from_def("#ffffff") == Color("#ffffff")
        assert color_from_def(Color("#ffffff")) == Color("#ffffff")
        assert color_from_def((255, 255, 255)) == Color("#ffffff")
