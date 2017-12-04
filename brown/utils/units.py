"""Various interoperable units classes and some related helper functions."""


class Unit:
    """An immutable graphical distance with a unit.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (`+`, `-`, `/`, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from brown.utils.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.0393701)

    If a `Unit` (or subclass) is to the left of an `int` or `float`,
    the value on the right will be converted to the left object's type
    before performing the operation. The resulting value will be a new
    object of the left-side object's type.

        >>> print(Inch(1) + 1)
        Inch(2)

    If an `int` or `float` are on the left hand side of any operator
    except `*`, `/`, or `//`, a TypeError will be raised.

        >>> print(2 * Inch(1))
        Inch(2)
        >>> print(1 + Inch(1))
        Traceback (most recent call last):
         ...
        TypeError: unsupported operand type(s) for +: 'int' and 'Inch'

    Warning: `Unit` objects are immutable. Any attempts to modify them
        in place will result in much sadness.
    """

    __slots__ = ('value',)

    CONVERSION_RATE = 1
    """float: the ratio of this class to `Unit`s.

    Subclasses should override this.
    """

    def __init__(self, value):
        """
        Args:
            value (int, float, or Unit): The value of the unit.
                `int` and `float` literals will be stored directly
                into `self.value`. Any value which is a unit subclass of
                `Unit` will be converted to that value in this unit.
        """
        if isinstance(value, (int, float)):
            self.value = value
        elif type(value) == type(self):
            # Same type as self, just duplicate value
            self.value = value.value
        elif isinstance(value, Unit):
            # Convertible type, so convert value
            self.value = (value._to_base_unit_float()
                          / self.CONVERSION_RATE)
            if isinstance(self.value, float) and self.value.is_integer():
                self.value = int(self.value)
        else:
            raise TypeError(
                'Cannot create {} from {}'.format(type(self).__name__,
                                                  type(value).__name__))

    ######## CONSTRUCTORS ########

    @classmethod
    def from_existing(cls, existing):
        """Clone any Unit object.

        Args:
            existing (Unit): An existing unit

        Returns: Unit
        """
        return type(existing)(existing.value)

    ######## PRIVATE METHODS ########

    def _to_base_unit_float(self):
        """Return this value as a float in base unit values.

        Returns: float
        """
        return self.value * self.CONVERSION_RATE

    def _assert_almost_equal(self, other, places=7):
        """Assert the near-equality of two units.

        **For testing purposes only.**

        Almost-equality is determined according to the base unit float
        representations of both units, within the accuracy of `places`.

        A helpful failure message is given in the event of failure.

        This is primarily for testing purposes, as the stdlib
        `assertAlmostEqual` doesn't play nice with custom numeric types.

        Args:
            other (Unit): The unit to compare against
            places (int): The number of decimal places of accuracy required.

        Raises:
            AssertionError: If failed.
        """
        if round(self._to_base_unit_float()
                 - other._to_base_unit_float(),
                 places) != 0:
            self_type = type(self)
            other_type = type(other)
            raise AssertionError(
                '{} and {} not equal within {} Unit decimal places.\n'
                'Both as {}: {} vs {}\n'
                'Both as {}: {} vs {}'.format(
                    self, other, places,
                    self_type.__name__, self, self_type(other),
                    other_type.__name__, other_type(self), other))

    ######## SPECIAL METHODS ########

    # Representations ---------------------------------------------------------

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.value)

    def __hash__(self):
        return hash(self.__repr__())

    # Comparisons -------------------------------------------------------------

    def __lt__(self, other):
        return self.value < type(self)(other).value

    def __le__(self, other):
        return self.value <= type(self)(other).value

    def __eq__(self, other):
        return (isinstance(other, (Unit, int, float))
                and self.value == type(self)(other).value)

    def __gt__(self, other):
        return self.value > type(self)(other).value

    def __ge__(self, other):
        return self.value >= type(self)(other).value

    # Operators ---------------------------------------------------------------

    def __add__(self, other):
        return type(self)(self.value + type(self)(other).value)

    def __sub__(self, other):
        return type(self)(self.value - type(self)(other).value)

    def __mul__(self, other):
        return type(self)(self.value * type(self)(other).value)

    def __truediv__(self, other):
        return type(self)(self.value / type(self)(other).value)

    def __floordiv__(self, other):
        return type(self)(self.value // type(self)(other).value)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return type(self)(self.value ** type(self)(other).value)
        else:
            return type(self)(
                pow(self.value, type(self)(other).value, modulo))

    def __neg__(self):
        return type(self)(-self.value)

    def __pos__(self):
        return type(self)(+self.value)

    def __abs__(self):
        return type(self)(abs(self.value))

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __round__(self, ndigits=None):
        return type(self)(round(self.value, ndigits))

    # Reverse Operators -------------------------------------------------------

    def __rmul__(self, other):
        return type(self)(other * self.value)

    def __rtruediv__(self, other):
        return type(self)(other / self.value)

    def __rfloordiv__(self, other):
        return type(self)(other // self.value)


class GraphicUnit(Unit):
    """A unit with a 1:1 ratio with Qt units.

    This will typically be the size of a pixel in `brown.show()` preview mode.

    In most cases, you probably want to use a more descriptive unit type.
    """
    CONVERSION_RATE = 1


class Inch(Unit):
    """An inch."""
    CONVERSION_RATE = 300


class Mm(Unit):
    """A millimeter."""
    CONVERSION_RATE = Inch.CONVERSION_RATE * 0.0393701


class Meter(Unit):
    """A meter."""
    CONVERSION_RATE = Mm.CONVERSION_RATE * 1000


def _convert_all_to_unit_in_immutable(iterable, unit):
    """Recursively convert all numbers in an immutable iterable.

    This is a helper function for convert_all_to_unit

    Args:
        iterable (Iterable): The immutable iterable to recursively convert
        unit (type): The unit to convert numerical elements to

    Returns:
        iter(any): An iterable the same type of the input.
            (set --> set, tuple --> tuple, etc.)
    """
    mutable_iterable = list(iterable)
    convert_all_to_unit(mutable_iterable, unit)
    return type(iterable)(mutable_iterable)


def convert_all_to_unit(iterable, unit):
    """Recursively convert all numbers found in an iterable to a unit in place.

    This function works in place. Immutable structures (namely tuples) found
    within `iterable` will be replaced. `iterable` itself may not be immutable.

    In dictionaries, *only values* will be converted. Keys will be left as-is.

    Args:
        iterable (Iterable): The iterable to recursively convert
        unit (type): The unit to convert numerical elements to

    Returns:
        None

    Raises:
        TypeError: If `iterable` is not an iterable or is immutable
    """
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if isinstance(value, (int, float, Unit)):
                iterable[key] = unit(value)
            elif isinstance(value, (list, dict)):
                convert_all_to_unit(iterable[key], unit)
            elif isinstance(value, (tuple, set)):
                iterable[key] = _convert_all_to_unit_in_immutable(
                    iterable[key], unit)
            # (else: continue --- nothing to do here)
    elif isinstance(iterable, list):
        for i in range(len(iterable)):
            if isinstance(iterable[i], (int, float, Unit)):
                iterable[i] = unit(iterable[i])
            elif isinstance(iterable[i], (list, dict)):
                convert_all_to_unit(iterable[i], unit)
            elif isinstance(iterable[i], (tuple, set)):
                iterable[i] = _convert_all_to_unit_in_immutable(
                    iterable[i], unit)
            # (else: continue --- nothing to do here)
    else:
        raise TypeError
