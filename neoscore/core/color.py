from __future__ import annotations

from typing import Tuple, Union

from typing_extensions import TypeAlias

from neoscore.core.exceptions import ColorBoundsError


class Color:
    """An 8-bit int RGBA color."""

    def __init__(self, *args):
        """
        Valid signatures:
            * Color(css_hex_string)
            * Color(red, green, blue)
            * Color(red, green, blue, alpha)
        """
        if len(args) == 1:
            self._set_with_hex(*args)
        elif len(args) == 3:
            self._set_with_rgb(*args)
        elif len(args) == 4:
            self._set_with_rgba(*args)
        else:
            raise TypeError("Invalid Color init args")

    @classmethod
    def from_def(cls, color_def: ColorDef) -> Color:
        if isinstance(color_def, Color):
            return color_def
        elif isinstance(color_def, tuple):
            return Color(*color_def)
        else:
            # otherwise color_def must be a str
            return Color(color_def)

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            type(self).__name__, self.red, self.green, self.blue, self.alpha
        )

    def __eq__(self, other):
        """Two Colors are considered equal if all of their properties are."""
        return (
            type(other) == type(self)
            and self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
            and self.alpha == other.alpha
        )

    def __hash__(self):
        """Colors with equal properties will have the same hash."""
        return 23467817 ^ self.red ^ self.green ^ self.blue ^ self.alpha

    @property
    def red(self):
        """int: The 0-255 value of the red color channel"""
        return self._red

    @property
    def green(self):
        """int: The 0-255 value of the green color channel"""
        return self._green

    @property
    def blue(self):
        """int: The 0-255 value of the blue color channel"""
        return self._blue

    @property
    def alpha(self):
        """int: The 0-255 value of the alpha color channel"""
        return self._alpha

    def _set_with_hex(self, hex_value):
        """Set properties from an #rrggbb hex string

        Args:
            hex_value (str): A CSS hex color string, with or without a leading '#'

        Returns: None
        """
        if hex_value.startswith("#"):
            hex_value = hex_value[1:]

        # Short or long form Hex
        if 3 <= len(hex_value) <= 4:
            self._red = int(hex_value[0] + (hex_value[0]), 16)
            self._green = int(hex_value[1] + (hex_value[1]), 16)
            self._blue = int(hex_value[2] + (hex_value[2]), 16)
            if len(hex_value) == 4:
                self._alpha = int(hex_value[3] + (hex_value[3]), 16)
            else:
                self._alpha = 255
        else:
            self._red = int(hex_value[0:2], 16)
            self._green = int(hex_value[2:4], 16)
            self._blue = int(hex_value[4:6], 16)
            if len(hex_value) == 8:
                self._alpha = int(hex_value[6:8], 16)
            else:
                self._alpha = 255

        self._validate_channel_values()

    def _set_with_rgb(self, red, green, blue):
        """Set properties from three 0-255 red, green, and blue values

        Args:
            red (int): A 0-255 red channel value
            green (int): A 0-255 green channel value
            blue (int): A 0-255 blue channel value

        Returns: None
        """
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = 255
        self._validate_channel_values()

    def _set_with_rgba(self, red, green, blue, alpha):
        """Set properties from four 0-255 red, green, blue, and alpha values

        Args:
            red (int): A 0-255 red channel value
            green (int): A 0-255 green channel value
            blue (int): A 0-255 blue channel value
            alpha (int): A 0-255 alpha channel value

        Returns: None
        """
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha
        self._validate_channel_values()

    def _validate_channel_values(self):
        for value in [self._red, self._green, self._blue, self._alpha]:
            if not (0 <= value <= 255):
                raise ColorBoundsError(value)


ColorDef: TypeAlias = Union[Color, str, Tuple[int, int, int], Tuple[int, int, int, int]]
"""A ``Color`` or a shorthand hex string or init argument tuple for one.

Hex strings may have 3 channels (#RRGGBB) or 4 (#RRGGBBAA).
"""
