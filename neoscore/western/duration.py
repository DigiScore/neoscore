from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from fractions import Fraction
from typing import Optional, Tuple, Union

from typing_extensions import TypeAlias

from neoscore.core.math_helpers import is_power_of_2
from neoscore.western.duration_display import DurationDisplay


@dataclass(frozen=True)
class Duration:
    """A metered non-tuplet duration.

    The duration fraction indicates duration as a fraction of a whole note.
    The actual written denomination of duration is deduced
    from the reduced fraction. For instance:

    * ``Duration(1, 4)`` indicates a quarter note value
    * ``Duration(1, 1)`` indicates a whole note value
    * ``Duration(3, 8)`` indicates a dotted quarter note value

    """

    numerator: InitVar[int]

    denominator: InitVar[int]

    fraction: Fraction = field(init=False)
    """The reduced fraction representation of the duration"""

    display: Optional[DurationDisplay] = field(init=False, compare=False)
    """The appearance spec of the duration when written in notes or rests.

    This is ``None`` if the duration cannot be represented without ties.
    """

    def __post_init__(self, numerator: int, denominator: int):
        if numerator <= 0:
            raise ValueError("Numerator must be positive")
        if not is_power_of_2(denominator):
            raise ValueError("Denominator must be a power of 2")
        super().__setattr__("fraction", Fraction(numerator, denominator))
        super().__setattr__("display", Duration._derive_display(self.fraction))

    @staticmethod
    def _derive_display(fraction: Fraction) -> Optional[DurationDisplay]:
        if fraction >= 2:
            if fraction >= 4:
                # Lengths >= 4 whole notes cannot be represented without a tie
                return None
            # The below algorithm doesn't work with double-breves, so
            # hack it by running it on fraction / 2, giving a
            # whole-note value, then plugging its dot count into the
            # result with double-breve (base_division 0) hardcoded
            sub_result = Duration._derive_display(fraction / 2)
            if sub_result is None:
                return None
            assert sub_result.base_duration == 1
            return DurationDisplay(0, sub_result.dot_count)
        partial_numerator: float = fraction.numerator
        partial_denominator: int = fraction.denominator
        dot_count = 0
        while partial_numerator > 1:
            partial_numerator = (partial_numerator - 1) / 2
            partial_denominator = partial_denominator // 2
            dot_count += 1
        if partial_numerator != 1:
            # Failure to reduce means the duration requires a tie to write
            return None
        return DurationDisplay(partial_denominator, dot_count)

    @classmethod
    def from_def(cls, duration_def: DurationDef) -> Duration:
        if isinstance(duration_def, Duration):
            return duration_def
        return Duration(*duration_def)

    @classmethod
    def from_description(cls, base_division: int, dots: int) -> Duration:
        """Create a ``Duration`` from a base division and a number of dots.

        ``Duration``\ s created with this will always have a valid ``DurationDisplay``.

        Args:
            base_division: Must be 0 (double whole note) or a power of 2
            dots: Must be >= 0
        """
        if base_division == 0:
            # double breve
            val = Fraction(2, 1)
            inc_division = 1
        elif is_power_of_2(base_division):
            val = Fraction(1, base_division)
            inc_division = base_division * 2
        else:
            raise ValueError("base_division must be 0 or a power of 2")
        for _ in range(dots):
            val += Fraction(1, inc_division)
            inc_division *= 2
        return Duration(val.numerator, val.denominator)

    @property
    def requires_tie(self) -> bool:
        """If this Duration requires a tie to be written."""
        return self.display is None

    def __float__(self):
        """Reduce the fractional representation to a ``float`` and return it."""
        return float(self.fraction)

    def __add__(self, other: Duration):
        """Durations are added by adding their fractions."""
        if not isinstance(other, type(self)):
            raise TypeError
        fraction_sum = self.fraction + other.fraction
        return Duration(fraction_sum.numerator, fraction_sum.denominator)

    def __sub__(self, other: Duration):
        """Durations are subtracted by subtracting their fractions."""
        if not isinstance(other, type(self)):
            raise TypeError
        fraction_diff = self.fraction - other.fraction
        return Duration(fraction_diff.numerator, fraction_diff.denominator)

    def __gt__(self, other: Duration):
        """Durations are compared by their fractions."""
        if not isinstance(other, type(self)):
            return False
        return self.fraction > other.fraction

    def __ge__(self, other: Duration):
        """Durations are compared by their fractions."""
        return self > other or self == other

    def __lt__(self, other: Duration):
        """Durations are ordered by their fractions."""
        if not isinstance(other, type(self)):
            return False
        return self.fraction < other.fraction

    def __le__(self, other: Duration):
        """Durations are compared by their fractions."""
        return self < other or self == other


DurationDef: TypeAlias = Union[Duration, Tuple[int, int]]
"""A Duration or a shorthand tuple for one."""
