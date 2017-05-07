from brown.utils.exceptions import ColorBoundsError


class Color:
    """A general purpose Color class"""

    def __init__(self, *args):
        """
        Valid signatures:
            * Color(red, green, blue)
            * Color(red, green, blue, alpha)
            * Color(hex_string)
            * Color(hex_string, alpha)

        Currently entering these values as keyword arguments
        is not supported.
        """
        if len(args) == 1:
            self._set_with_hex(*args)
        elif len(args) == 2:
            self._set_with_hex_alpha(*args)
        elif len(args) == 3:
            self._set_with_rgb(*args)
        elif len(args) == 4:
            self._set_with_rgba(*args)
        else:
            raise TypeError('Expected between 1 and 4 arguments, '
                            'got {}'.format(len(args)))

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(type(self).__name__,
                                           self.red,
                                           self.green,
                                           self.blue,
                                           self.alpha)

    def __eq__(self, other):
        """Two Colors are considered equal if all of their properties are."""
        return (type(other) == type(self) and
                self.red == other.red and
                self.green == other.green and
                self.blue == other.blue and
                self.alpha == other.alpha)

    def __hash__(self):
        """A Color's hash is a hash of its __repr__().

        Colors with equal properties will have the same hash.
        """
        return hash(self.__repr__())

    ######## PUBLIC PROPERTIES ########

    @property
    def red(self):
        """int: The 0-255 value of the red color channel"""
        return self._red

    @red.setter
    def red(self, value):
        if not (0 <= value <= 255):
            raise ColorBoundsError('red', value)
        self._red = int(value)

    @property
    def green(self):
        """int: The 0-255 value of the green color channel"""
        return self._green

    @green.setter
    def green(self, value):
        if not (0 <= value <= 255):
            raise ColorBoundsError('green', value)
        self._green = int(value)

    @property
    def blue(self):
        """int: The 0-255 value of the blue color channel"""
        return self._blue

    @blue.setter
    def blue(self, value):
        if not (0 <= value <= 255):
            raise ColorBoundsError('blue', value)
        self._blue = int(value)

    @property
    def alpha(self):
        """int: The 0-255 value of the alpha color channel"""
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if not (0 <= value <= 255):
            raise ColorBoundsError('alpha', value)
        self._alpha = int(value)

    ######## PRIVATE METHODS ########

    def _set_with_hex(self, hex_value):
        """Set properties from an #rrggbb hex string

        Args:
            hex_value (str): A hexadecimal color string with 6 characters
                (or 7 if including a leading "#")

        Returns: None
        """
        if hex_value.startswith('#'):
            hex_value = hex_value[1:]
        self.red = int(hex_value[0:2], 16)
        self.green = int(hex_value[2:4], 16)
        self.blue = int(hex_value[4:6], 16)
        self.alpha = 255

    def _set_with_hex_alpha(self, hex_value, alpha):
        """Set properties from an #rrggbb hex string and a 0-255 alpha value

        Args:
            hex_value (str): A hexadecimal color string with 6 characters
                (or 7 if including a leading "#")
            alpha (int): A 0-255 alpha channel value

        Returns: None
        """
        self._set_with_hex(hex_value)
        self.alpha = alpha

    def _set_with_rgb(self, red, green, blue):
        """Set properties from three 0-255 red, green, and blue values

        Args:
            red (int): A 0-255 red channel value
            green (int): A 0-255 green channel value
            blue (int): A 0-255 blue channel value

        Returns: None
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = 255

    def _set_with_rgba(self, red, green, blue, alpha):
        """Set properties from four 0-255 red, green, blue, and alpha values

        Args:
            red (int): A 0-255 red channel value
            green (int): A 0-255 green channel value
            blue (int): A 0-255 blue channel value
            alpha (int): A 0-255 alpha channel value

        Returns: None
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
