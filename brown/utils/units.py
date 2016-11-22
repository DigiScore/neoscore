"""Various interoperable units classes"""


class Unit:
    """
    A fundamental base unit acting as a common ground for unit conversions.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (`+`, `-`, `/`, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from brown.utils.inch import Inch
        >>> from brown.utils.mm import Mm
        >>> print(Inch(1) + Mm(1))
        1.0393700787401574 inches

    If a `Unit` (or subclass) is to the left of an `int` or `float`,
    the value on the right will be converted to the left object's type
    before performing the operation. The resulting value will be a new
    object of the left-side object's type.

        >>> print(Inch(1) + 1)
        2 inches

    If an `int` or `float` are on the left hand side of any operator
    except `*`, `/`, or `//`, a TypeError will be raised.

        >>> print(2 * Inch(1))
        2 inches
        >>> print(1 + Inch(1))
        Traceback (most recent call last):
         ...
        TypeError: unsupported operand type(s) for +: 'int' and 'Inch'
    """

    # For use in __str__(). Subclasses should override this.
    _unit_name_plural = 'base units'
    # Ratio of this class's units to Units.
    # Subclasses should override this.
    _base_units_per_self_unit = 1

    def __init__(self, value):
        """
        Args:
            value (int, float, Unit): The value of the unit.
                `int` and `float` literals will be stored directly
                into `self.value`. Any value which is a unit subclass of
                `Unit` will be converted to that value in this unit.
        """
        if not type(self)._is_acceptable_type(value):
            raise TypeError(
                'Unsupported value type "{}"'.format(type(value).__name__))
        if isinstance(value, (int, float)):
            self.value = value
        elif type(value) == type(self):
            # Same type as self, just duplicate value
            self.value = value.value
        elif isinstance(value, Unit):
            # Convertible type, so convert value
            self.value = ((value._base_units_per_self_unit * value.value) /
                          self._base_units_per_self_unit)
            if isinstance(self.value, float) and self.value.is_integer():
                self.value = int(self.value)
        else:
            raise AssertionError('Leaky type in Unit. This is a bug!')

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def _is_acceptable_type(cls, value):
        """Tell if an object can be converted to this unit.

        Args:
            value (Any): The value to test

        Returns:
            bool
        """
        return isinstance(value, (int, float, Unit))

    ######## SPECIAL METHODS ########

    def __str__(self):
        return '{} {}'.format(self.value, self._unit_name_plural)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.value)

    # Comparisons -------------------------------------------------------------

    def __lt__(self, other):
        return self.value < self.__class__(other).value

    def __le__(self, other):
        return self.value <= self.__class__(other).value

    def __eq__(self, other):
        return self.value == self.__class__(other).value

    def __ne__(self, other):
        return self.value != self.__class__(other).value

    def __gt__(self, other):
        return self.value > self.__class__(other).value

    def __ge__(self, other):
        return self.value >= self.__class__(other).value

    # Operators ---------------------------------------------------------------

    def __add__(self, other):
        return self.__class__(self.value + self.__class__(other).value)

    def __sub__(self, other):
        return self.__class__(self.value - self.__class__(other).value)

    def __mul__(self, other):
        return self.__class__(self.value * self.__class__(other).value)

    def __truediv__(self, other):
        return self.__class__(self.value / self.__class__(other).value)

    def __floordiv__(self, other):
        return self.__class__(self.value // self.__class__(other).value)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return self.__class__(self.value ** self.__class__(other).value)
        else:
            return self.__class__(
                pow(self.value, self.__class__(other).value, modulo))

    def __neg__(self):
        return self.__class__(-self.value)

    def __pos__(self):
        return self.__class__(+self.value)

    def __abs__(self):
        return self.__class__(abs(self.value))

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __round__(self, ndigits=None):
        return self.__class__(round(self.value, ndigits))

    # Reverse Operators -------------------------------------------------------

    def __rmul__(self, other):
        return self.__class__(other * self.value)

    def __rtruediv__(self, other):
        return self.__class__(other / self.value)

    def __rfloordiv__(self, other):
        return self.__class__(other // self.value)


class GraphicUnit(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _unit_name_plural = 'pixels'
    _base_units_per_self_unit = 1

    # (all other functionality implemented in Unit)
    pass


class Inch(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _unit_name_plural = 'inches'
    _base_units_per_self_unit = 300

    # (all other functionality implemented in Unit)
    pass


class Mm(Unit):
    # TODO: When stable, copy and tailor docstring from Unit
    _unit_name_plural = 'millimeters'
    _base_units_per_self_unit = 11.811023622047244

    # (all other functionality implemented in Unit)
    pass
