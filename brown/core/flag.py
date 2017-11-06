from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.utils.exceptions import NoFlagNeededError
from brown.utils.point import Point
from brown.utils.units import Unit


class Flag(MusicText, StaffObject):

    """A simple Flag glyph with a duration and direction

    This is meant to be attached to a Stem end_point.
    As a result, Flags are positioned at (0, 0) relative to their parent.
    """

    _up_glyphnames = {
        1024: 'flag1024thUp',
        512: 'flag512thUp',
        256: 'flag256thUp',
        128: 'flag128thUp',
        64: 'flag64thUp',
        32: 'flag32ndUp',
        16: 'flag16thUp',
        8: 'flag8thUp',
    }
    _down_glyphnames = {
        1024: 'flag1024thDown',
        512: 'flag512thDown',
        256: 'flag256thDown',
        128: 'flag128thDown',
        64: 'flag64thDown',
        32: 'flag32ndDown',
        16: 'flag16thDown',
        8: 'flag8thDown',
    }

    def __init__(self, duration, direction, parent):
        """
        Args:
            duration (Beat):
            direction (int): The direction of the flag, where
                -1 indicates pointing upward, and 1 vice versa.
            parent (StaffObject or Staff)
        """
        self.duration = duration
        self.direction = direction
        if self.direction == 1:
            glyph_name = self._down_glyphnames[self.duration.base_division]
        else:
            glyph_name = self._up_glyphnames[self.duration.base_division]
        MusicText.__init__(self,
                           Point(Unit(0), Unit(0)),
                           [glyph_name],
                           parent)
        StaffObject.__init__(self, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self):
        """Beat: The time duration of this object"""
        return self._duration

    @duration.setter
    def duration(self, value):
        if not self.needs_flag(value):
            raise NoFlagNeededError(value)
        self._duration = value

    @property
    def direction(self):
        """int: The flag direction, where -1 points up and 1 points down.

        Setting to values other than -1 and 1 will raise a ValueError.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        if not (value == 1 or value == -1):
            raise ValueError('Flag.direction must be 1 or -1')
        else:
            self._direction = value

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def needs_flag(cls, duration):
        """Determine if a Beat needs a flag.

        Args:
            duration (Beat): The Duration to check

        Returns: bool
        """
        return (duration.base_division in cls._up_glyphnames)

    @classmethod
    def vertical_offset_needed(cls, duration, staff_unit):
        """Find the space needed in a stem using a flag of a given duration

        Args:
            duration (Beat): The duration for the hypothetical flag
            staff_unit (type): The staff unit to give the result in

        Returns: StaffUnit
        """
        if cls.needs_flag(duration):
            return staff_unit(1)
        else:
            return staff_unit(0)
