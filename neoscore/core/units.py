"""Various interoperable units classes and some related helper functions."""
from __future__ import annotations

from typing import Any, Optional, Type, TypeVar, Union, cast

TUnit = TypeVar("TUnit", bound="Unit")


class Unit:
    """An immutable graphical distance with a unit.

    Unit objects enable easy conversion from one unit to another and
    convenient operations between them.

    Common operators (``+``, ``-``, ``/``, etc.) are supported between them.
    Return values from these operations are given in the type on the left.

        >>> from neoscore.core.units import Inch, Mm
        >>> print(Inch(1) + Mm(1))
        Inch(1.039)

    To facilitate easy comparison between equivalent values in
    different units, equality is checked with a tolerance of
    ``Unit(0.001)``.

        >>> from neoscore.core.units import Inch, Mm
        >>> assert Inch(Mm(1)) == Mm(1)
        >>> assert Inch(Mm(1)) >= Mm(1)
        >>> assert Inch(Mm(1)) <= Mm(1)

    """

    __slots__ = ("base_value", "_display_value")

    CONVERSION_RATE: float = 1
    """The ratio of this class to fundamental ``Unit``\ s.

    Subclasses should override this.
    """

    def __init__(self, value, _raw_base_value=None):
        if _raw_base_value is not None:
            # Short circuiting constructor for internal use
            self.base_value = _raw_base_value
            self._display_value = None
        else:
            base_value = getattr(value, "base_value", None)
            if base_value is not None:
                self.base_value = base_value
                self._display_value = None
            else:
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

    @property
    def rounded_base_value(self) -> float:
        """The base value rounded to 2 decimal places.

        This is useful for things like hash keys for caching purposes
        """
        return round(self.base_value, 2)

    ######## SPECIAL METHODS ########

    # Representations ---------------------------------------------------------

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.display_value)

    # Comparisons -------------------------------------------------------------

    _CMP_POS_EPSILON = 0.001
    _CMP_NEG_EPSILON = -0.001

    def __lt__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_NEG_EPSILON

    def __le__(self, other: Unit):
        return self.base_value - other.base_value < Unit._CMP_POS_EPSILON

    def __eq__(self, other: Any):
        """Two units are equal if the difference between their base
        values is less than 0.001, or if both are infinite.
        """
        return hasattr(other, "base_value") and (
            # Check strict equality first for speed and coverage of infinity values
            self.base_value == other.base_value
            or abs(self.base_value - other.base_value) < Unit._CMP_POS_EPSILON
        )

    def __gt__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_POS_EPSILON

    def __ge__(self, other: Unit):
        return self.base_value - other.base_value > Unit._CMP_NEG_EPSILON

    # Operators ---------------------------------------------------------------

    def __add__(self: TUnit, other: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=self.base_value + other.base_value)

    def __sub__(self: TUnit, other: Unit) -> TUnit:
        return type(self)(None, _raw_base_value=self.base_value - other.base_value)

    def __mul__(self: TUnit, other: float) -> TUnit:
        if hasattr(other, "base_value"):
            raise TypeError
        return type(self)(None, _raw_base_value=self.base_value * other)

    def __rmul__(self: TUnit, other: float) -> TUnit:
        # __rmul__ behaves identically to __mul__
        if hasattr(other, "base_value"):
            raise TypeError
        return type(self)(None, _raw_base_value=self.base_value * other)

    def __truediv__(self: TUnit, other: Union[Unit, float]) -> Union[TUnit, float]:
        if hasattr(other, "base_value"):
            # Unit / Unit -> Float
            return self.base_value / (cast(Unit, other)).base_value
        # Unit / Float -> Unit
        return type(self)(None, _raw_base_value=self.base_value / other)

    def __pow__(self: TUnit, other: float, modulo: Optional[int] = None) -> TUnit:
        return type(self)(Unit(pow(self.base_value, other, modulo)))

    def __neg__(self: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=-self.base_value)

    def __pos__(self: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=+self.base_value)

    def __abs__(self: TUnit) -> TUnit:
        return type(self)(None, _raw_base_value=abs(self.base_value))


# TODO HIGH delete this????
class GraphicUnit(Unit):
    """A unit with a 1:1 ratio with Qt units.

    This will typically be the size of a pixel in ``neoscore.show()`` preview mode.

    In most cases, you probably want to use a more descriptive unit type.
    """

    CONVERSION_RATE = 1


class Inch(Unit):
    """An inch."""

    CONVERSION_RATE = 72


class Mm(Unit):
    """A millimeter."""

    CONVERSION_RATE = Inch.CONVERSION_RATE * 0.0393701


# Constants

ZERO = Unit(0)
"""Shorthand for a zero unit"""

# Utilities


def make_unit_class(name, unit_size):
    return type(
        name,
        (Unit,),
        {"CONVERSION_RATE": unit_size},
    )


def _convert_all_to_unit_out_of_place(
    collection: Union[tuple, set], unit: Type[Unit]
) -> Union[tuple, set]:
    mutable_iterable: list[Any] = list(collection)
    convert_all_to_unit(mutable_iterable, unit)
    return type(collection)(mutable_iterable)


def convert_all_to_unit(collection: Union[list, dict], unit: Type[Unit]):
    """Recursively convert all numbers found in a list or dict to a unit in place.

    This function works in place. Tuples and sets found
    within ``collection`` will be replaced.

    In dictionaries, only values are converted.
    """
    if isinstance(collection, dict):
        for key, value in collection.items():
            if isinstance(value, (int, float, Unit)):
                collection[key] = unit(value)
            elif isinstance(value, (list, dict)):
                convert_all_to_unit(collection[key], unit)
            elif isinstance(value, (tuple, set)):
                collection[key] = _convert_all_to_unit_out_of_place(
                    collection[key], unit
                )
            # (else: continue --- nothing to do here)
    elif isinstance(collection, list):
        for i in range(len(collection)):
            if isinstance(collection[i], (int, float, Unit)):
                collection[i] = unit(collection[i])
            elif isinstance(collection[i], (list, dict)):
                convert_all_to_unit(collection[i], unit)
            elif isinstance(collection[i], (tuple, set)):
                collection[i] = _convert_all_to_unit_out_of_place(collection[i], unit)
            # (else: continue --- nothing to do here)
    else:
        raise TypeError
