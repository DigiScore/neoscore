import unittest

import pytest

from neoscore.core.color import Color, ColorBoundsError


class TestColor(unittest.TestCase):
    def test_init_with_hex_string(self):
        color = Color("eeddcc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_hex_string_with_leading_hash(self):
        color = Color("#eeddcc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_8_digit_hex_string(self):
        color = Color("eeddcc11")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 17

    def test_init_with_8_digit_hex_string_and_leading_hash(self):
        color = Color("#eeddcc11")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 17

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

    def test_init_with_short_hex_string_and_leading_hash(self):
        color = Color("#edc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_short_hex_string_and_no_leading_hash(self):
        color = Color("edc")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 255

    def test_init_with_4_digit_short_hex_string_and_leading_hash(self):
        color = Color("#edc1")
        assert color.red == 238
        assert color.green == 221
        assert color.blue == 204
        assert color.alpha == 17

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

    def test_from_def(self):
        assert Color.from_def("#ffffff") == Color("#ffffff")
        assert Color.from_def(Color("#ffffff")) == Color("#ffffff")
        assert Color.from_def((255, 255, 255)) == Color("#ffffff")
        assert Color.from_def("#fff") == Color("#ffffff")

    def test_color_is_immutable(self):
        color = Color("#ffffff")
        with pytest.raises(AttributeError):
            color.red = 123  # noqa
        with pytest.raises(AttributeError):
            color.green = 123  # noqa
        with pytest.raises(AttributeError):
            color.blue = 123  # noqa
        with pytest.raises(AttributeError):
            color.alpha = 123  # noqa
