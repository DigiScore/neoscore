import re

from neoscore.core.directions import DirectionY
from neoscore.core.exceptions import InvalidIntervalError


class Interval:
    """An abstract pitch interval."""

    _shorthand_regex = re.compile("^([ad])([mMPdA])([1-9]\d*)$")
    _base_pc_deltas = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    _qualities_in_english = {
        "m": "minor",
        "M": "Major",
        "d": "diminished",
        "A": "Augmented",
    }
    _perfectable_distances = [1, 4, 5]

    def __init__(self, specifier: str):
        """
        The interval specifier should be a string in the form:
        ``[direction][quality][distance]`` where:

        * ``direction`` is one of:

            * ``'a'`` for ascending
            * ``'d'`` for descending

        * ``quality`` is one of:

            * ``'m'`` for minor
            * ``'M'`` for Major
            * ``'P'`` for Perfect
            * ``'d'`` for diminished
            * ``'A'`` for Augmented

        * ``distance`` is any positive integer indicating the
          interval distance.

        Some examples:

            * ``Interval('aM3')`` signifies an ascending major third
            * ``Interval('dA9')`` signifies a descending augmented ninth
        """
        match = Interval._shorthand_regex.match(specifier)
        if match is None:
            raise InvalidIntervalError
        self._direction = DirectionY.UP if match.group(1) == "a" else DirectionY.DOWN
        self._quality = match.group(2)
        self._distance = int(match.group(3))
        # Check against invalid edge case intervals
        if (
            self.simple_distance in Interval._perfectable_distances
            and self._quality
            not in [
                "P",
                "d",
                "A",
            ]
        ):
            # unisons, fourths, fifths, and their compounds
            # can only be perfect, augmented, or diminished
            raise InvalidIntervalError

    def __repr__(self):
        direction_str = "a" if self.direction == DirectionY.UP else "d"
        return f"Interval('{direction_str}{self.quality}{self.distance}')"

    def __hash__(self):
        return hash(self.direction) ^ hash(self.quality) ^ hash(self.distance)

    def __eq__(self, other):
        return (
            isinstance(other, Interval)
            and self.direction == other.direction
            and self.quality == other.quality
            and self.distance == other.distance
        )

    @property
    def direction(self) -> DirectionY:
        return self._direction

    @property
    def quality(self) -> str:
        return self._quality

    @property
    def quality_in_english(self) -> str:
        return Interval._qualities_in_english[self._quality]

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def staff_distance(self) -> float:
        """The vertical offset needed to show this interval on a staff.

        The value is given in pseudo-staff-units.

        >>> Interval('aM3').staff_distance
        -1.0
        >>> Interval('dm3').staff_distance
        1.0
        >>> Interval('aP1').staff_distance
        0.0
        >>> Interval('dP8').staff_distance
        3.5
        """
        return ((self.distance - 1) * self.direction.value) / 2

    @property
    def simple_distance(self) -> float:
        """The simplified interval distance collapsing compound intervals.

        This value is the simplified version of ``self.distance`` where intervals
        larger than an octave are moved to be within one octave.

        Examples:
            >>> Interval('aM10').simple_distance
            3
            >>> Interval('dP12').simple_distance
            5
        """
        return ((self.distance - 1) % 7) + 1
