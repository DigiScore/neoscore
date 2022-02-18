"""Various interoperable units classes and some related helper functions."""

# This is needed to support function argument annotations referencing
# the containing class. (This is not supposed to be needed in Python
# 3.10, but for some reason in my 3.10.2 environment it's still
# needed)
from __future__ import annotations

from typing import Any, TypeVar, Union

TUnit = TypeVar("TUnit", bound="Unit")


class Unit:
    """An immutable graphical distance with a unit.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (`+`, `-`, `/`, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from brown.utils.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.039)
    """

    __slots__ = ("base_value", "_display_value")

    CONVERSION_RATE = 1
    """float: the ratio of this class to `Unit`s.

    Subclasses should override this.
    """

    def __init__(self, value):
        base_value = getattr(value, "base_value", None)
        if base_value is not None:
            self.base_value = base_value
            self._display_value = None
        else:
            # TODO document this base_value rounding behavior - it's
            # needed to allow ergonomic comparisons between units
            # without floating point errors getting in the way.
            #
            # Also need to determine if this is the best approach -
            # might be better to defer rounding to comparison
            # operators to minimize error accumulation and avoid
            # unecessary computation.
            self.base_value = value * self.CONVERSION_RATE
            self._display_value = value

    @property
    def display_value(self) -> float:
        """The readable given value in the unit.

        If the unit was constructed with a simple number (e.g. Mm(1))
        this will return the exact given argument value. If the unit
        was constructed from another unit (e.g. Mm(Inch(1))) this will
        return the converted value rounded to 3 decimal places. This
        is helpful for correcting floating point math errors.
        """
        if self._display_value:
            return self._display_value
        return round(self.base_value / self.CONVERSION_RATE, 3)

    ######## SPECIAL METHODS ########

    # Representations ---------------------------------------------------------

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.display_value)

    def __hash__(self):
        return hash(self.base_value)

    # Comparisons -------------------------------------------------------------

    _CMP_POS_EPSILON = 0.001
    _CMP_NEG_EPSILON = -0.001

    # TODO document unit comparison behavior and subtleties

    def __lt__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_NEG_EPSILON

    def __le__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_POS_EPSILON

    def __eq__(self, other: Any):
        """Two units are equal if the difference between their base
        values is less than 0.001, or if both are infinite.
        """
        return hasattr(other, "base_value") and (
            abs(self.base_value - other.base_value) < Unit._CMP_POS_EPSILON
            # Do strict equality check to cover inf == inf
            or self.base_value == other.base_value
        )

    def __gt__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_POS_EPSILON

    def __ge__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_NEG_EPSILON

    # Operators ---------------------------------------------------------------

    def __add__(self, other: Unit) -> TUnit:
        return type(self)(Unit(self.base_value + other.base_value))

    def __sub__(self, other: Unit) -> TUnit:
        return type(self)(Unit(self.base_value - other.base_value))

    def __mul__(self, other: float) -> TUnit:
        return type(self)(Unit(self.base_value * other))

    def __truediv__(self, other: Union[Unit, float]) -> Union[TUnit, float]:
        if hasattr(other, "base_value"):
            # Unit / Unit -> Float
            return self.base_value / other.base_value
        # Unit / Float -> Unit
        return type(self)(Unit(self.base_value / other))

    def __pow__(self, other: float, modulo: Optional[int] = None) -> TUnit:
        return type(self)(Unit(pow(self.base_value, other, modulo)))

    def __neg__(self) -> TUnit:
        return type(self)(Unit(-self.base_value))

    def __pos__(self) -> TUnit:
        return type(self)(Unit(+self.base_value))

    def __abs__(self) -> TUnit:
        return type(self)(Unit(abs(self.base_value)))

    # TODO maybe restore support for __rmul__


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


def make_unit_class(name, unit_size):
    return type(
        name,
        (Unit,),
        {"CONVERSION_RATE": unit_size},
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
