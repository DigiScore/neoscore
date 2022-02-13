"""Various interoperable units classes and some related helper functions."""

# This is needed to support function argument annotations referencing
# the containing class. (This is not supposed to be needed in Python
# 3.10, but for some reason in my 3.10.2 environment it's still
# needed)
from __future__ import annotations

from typing import Any, TypeVar, Union

_LAST_TYPE_ID = -1


def _next_type_id():
    global _LAST_TYPE_ID
    _LAST_TYPE_ID += 1
    return _LAST_TYPE_ID


TUnit = TypeVar("TUnit", bound="Unit")


class Unit:
    """An immutable graphical distance with a unit.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (`+`, `-`, `/`, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from brown.utils.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.0393701)
    """

    __slots__ = ("value",)

    CONVERSION_RATE = 1
    """float: the ratio of this class to `Unit`s.

    Subclasses should override this.
    """

    _TYPE_ID = _next_type_id()
    """int: a unique ID number for this Unit type.

    This is used to optimize type comparisons. Each Unit class must
    fetch a unique value using `_next_type_id()`.
    """

    def __init__(self, value):
        """
        Args:
            value (int, float, or Unit): The value of the unit.
                `int` and `float` literals will be stored directly
                into `self.value`. Any value which is a unit subclass of
                `Unit` will be converted to that value in this unit.
        """
        if hasattr(value, "_TYPE_ID"):
            if value._TYPE_ID == self._TYPE_ID:
                self.value = value.value
            else:
                self.value = value._in_base_unit_float / self.CONVERSION_RATE
        else:
            self.value = value

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

    @property
    def _in_base_unit_float(self):
        """Return this value as a float in base unit values.

        Returns: float
        """
        return self.value * self.CONVERSION_RATE

    ######## SPECIAL METHODS ########

    # Representations ---------------------------------------------------------

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)

    def __hash__(self):
        # Add a random constant to prevent collisions with simple numbers
        return 8726347 ^ hash(self._in_base_unit_float)

    # Comparisons -------------------------------------------------------------

    def __lt__(self, other: Unit):
        if self._TYPE_ID == other._TYPE_ID:
            return self.value < other.value
        return self._in_base_unit_float < other._in_base_unit_float

    def __le__(self, other: Unit):
        if self._TYPE_ID == other._TYPE_ID:
            return self.value <= other.value
        return self._in_base_unit_float <= other._in_base_unit_float

    def __eq__(self, other: Any):
        return hasattr(other, "_TYPE_ID") and self.value == type(self)(other).value

    def __gt__(self, other: Unit):
        if self._TYPE_ID == other._TYPE_ID:
            return self.value > other.value
        return self._in_base_unit_float > other._in_base_unit_float

    def __ge__(self, other: Unit):
        if self._TYPE_ID == other._TYPE_ID:
            return self.value >= other.value
        return self._in_base_unit_float >= other._in_base_unit_float

    # Operators ---------------------------------------------------------------

    def __add__(self, other: Unit) -> TUnit:
        if self._TYPE_ID == other._TYPE_ID:
            return type(self)(self.value + other.value)
        return type(self)(
            self.value + (other._in_base_unit_float / self.CONVERSION_RATE)
        )

    def __sub__(self, other: Unit) -> TUnit:
        if self._TYPE_ID == other._TYPE_ID:
            return type(self)(self.value - other.value)
        return type(self)(
            self.value - (other._in_base_unit_float / self.CONVERSION_RATE)
        )

    def __mul__(self, other: Union[Unit, float]) -> TUnit:
        return type(self)(self.value * type(self)(other).value)

    def __truediv__(self, other: Union[Unit, float]) -> Union[TUnit, float]:
        if hasattr(other, "_TYPE_ID"):
            # Unit / Unit -> Float
            if self._TYPE_ID == other._TYPE_ID:
                return self.value / other.value
            return self._in_base_unit_float / other._in_base_unit_float
        # Unit / Float -> Unit
        return type(self)(self.value / other)

    def __pow__(self, other: float, modulo: Optional[int] = None) -> TUnit:
        return type(self)(pow(self.value, other, modulo))

    def __neg__(self) -> TUnit:
        return type(self)(-self.value)

    def __pos__(self) -> TUnit:
        return type(self)(+self.value)

    def __abs__(self) -> TUnit:
        return type(self)(abs(self.value))

    # TODO maybe restore support for __rmul__


class GraphicUnit(Unit):
    """A unit with a 1:1 ratio with Qt units.

    This will typically be the size of a pixel in `brown.show()` preview mode.

    In most cases, you probably want to use a more descriptive unit type.
    """

    CONVERSION_RATE = 1
    _TYPE_ID = _next_type_id()


class Inch(Unit):
    """An inch."""

    CONVERSION_RATE = 300
    _TYPE_ID = _next_type_id()


class Mm(Unit):
    """A millimeter."""

    CONVERSION_RATE = Inch.CONVERSION_RATE * 0.0393701
    _TYPE_ID = _next_type_id()


class Meter(Unit):
    """A meter."""

    CONVERSION_RATE = Mm.CONVERSION_RATE * 1000
    _TYPE_ID = _next_type_id()


def make_unit_class(name, unit_size):
    return type(
        name,
        (Unit,),
        {"CONVERSION_RATE": Unit(unit_size).value, "_TYPE_ID": _next_type_id()},
    )


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


# TODO This should be refactored to be out-of-place to prevent
# dangerous antipatterns as discovered in MusicFont
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
                iterable[key] = _convert_all_to_unit_in_immutable(iterable[key], unit)
            # (else: continue --- nothing to do here)
    elif isinstance(iterable, list):
        for i in range(len(iterable)):
            if isinstance(iterable[i], (int, float, Unit)):
                iterable[i] = unit(iterable[i])
            elif isinstance(iterable[i], (list, dict)):
                convert_all_to_unit(iterable[i], unit)
            elif isinstance(iterable[i], (tuple, set)):
                iterable[i] = _convert_all_to_unit_in_immutable(iterable[i], unit)
            # (else: continue --- nothing to do here)
    else:
        raise TypeError
