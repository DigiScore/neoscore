import re

from brown.utils.exceptions import InvalidIntervalError


class Interval:
    """A pitch interval."""
    _shorthand_regex = re.compile("^([ad])([mMPdA])([1-9]\d*)$")
    _base_pc_deltas = {
        1: 0,
        2: 2,
        3: 4,
        4: 5,
        5: 7,
        6: 9,
        7: 11
    }
    _qualities_in_english = {
        'm': 'minor',
        'M': 'Major',
        'd': 'diminished',
        'A': 'Augmented'
    }
    _perfectable_distances = [1, 4, 5]

    def __init__(self, specifier):
        """
        Args:
            specifier (str): A description of the interval.

        The interval specifier should be a string in the form:
        `[direction][quality][distance]` where:
            * `direction` is one of:
              * `'a'` for ascending
              * `'d'` for descending
            * `quality` is one of:
              * `'m'` for minor
              * `'M'` for Major
              * `'P'` for Perfect
              * `'d'` for diminished
              * `'A'` for Augmented
            * `distance` is any positive integer indicating the
              interval distance.

        Some examples:

            * `Interval('aM3')` signifies an ascending major third
            * `Interval('dA9')` signifies a descending augmented ninth
        """
        match = Interval._shorthand_regex.match(specifier)
        if match is None:
            raise InvalidIntervalError
        direction = match.group(1)
        quality = match.group(2)
        distance = int(match.group(3))
        self._direction = direction
        self._quality = quality
        self._distance = distance
        # Check against invalid edge case intervals
        if (self.simple_distance in Interval._perfectable_distances and
                quality not in ['P', 'd', 'A']):
            # unisons, fourths, fifths, and their compounds
            # can only be perfect, augmented, or diminished
            raise InvalidIntervalError

    ######## PUBLIC PROPERTIES ########

    @property
    def direction(self):
        return self._direction

    @property
    def direction_as_int(self):
        return -1 if self._direction == 'd' else 1

    @property
    def quality(self):
        return self._quality

    @property
    def quality_in_english(self):
        return Interval._qualities_in_english[self._quality]

    @property
    def distance(self):
        # TODO: Roll distance and direction together into a pos/neg int?
        return self._distance

    @property
    def staff_distance(self):
        """float: The number of staff units covered by this interval.

        If this value is converted to a StaffUnit, it will give the
        vertical distance from the starting note to ending note on
        the staff, where 1 is the distance between two staff lines.

        Note that the interval quality has no effect on this property.

        >>> Interval('aM3').staff_distance
        1.0
        >>> Interval('dm3').staff_distance
        -1.0
        >>> Interval('aP1').staff_distance
        0.0
        >>> Interval('dP8').staff_distance
        -3.5
        """
        return (((self.distance - 1) * self.direction_as_int) / 2)

    @property
    def simple_distance(self):
        """float: The simplified interval distance collapsing compound intervals.

        This value is the simplified version of `self.distance` where intervals
        larger than an octave are moved to be within one octave.

        Examples:
            >>> Interval('aM10').simple_distance
            3
            >>> Interval('dP12').simple_distance
            5
        """
        return ((self.distance - 1) % 7) + 1

    @property
    def pitch_class_delta(self):
        octave = (self.distance - 1) // 7
        octave_pc_dist = octave * 12
        simple_pc_dist = Interval._base_pc_deltas[self.simple_distance]
        if self.simple_distance in Interval._perfectable_distances:
            if self.quality == 'd':
                simple_pc_dist -= 1
            elif self.quality == 'A':
                simple_pc_dist += 1
            # Otherwise perfect - no modification needed
        else:
            if self.quality == 'd':
                simple_pc_dist -= 2
            elif self.quality == 'm':
                simple_pc_dist -= 1
            elif self.quality == 'A':
                simple_pc_dist += 1
            # Otherwise major - no modification needed
        return (octave_pc_dist + simple_pc_dist) * self.direction_as_int
