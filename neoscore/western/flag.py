from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject
from neoscore.models.beat import Beat
from neoscore.models.vertical_direction import VerticalDirection
from neoscore.utils.exceptions import NoFlagNeededError
from neoscore.utils.point import PointDef
from neoscore.western.staff_object import StaffObject


class Flag(MusicText, StaffObject):

    """A simple Flag glyph with a duration and direction"""

    _up_glyphnames = {
        1024: "flag1024thUp",
        512: "flag512thUp",
        256: "flag256thUp",
        128: "flag128thUp",
        64: "flag64thUp",
        32: "flag32ndUp",
        16: "flag16thUp",
        8: "flag8thUp",
    }
    _down_glyphnames = {
        1024: "flag1024thDown",
        512: "flag512thDown",
        256: "flag256thDown",
        128: "flag128thDown",
        64: "flag64thDown",
        32: "flag32ndDown",
        16: "flag16thDown",
        8: "flag8thDown",
    }

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        duration: Beat,
        direction: VerticalDirection,
    ):
        """
        Args:
            pos: The position of this flag. When `parent` is a stem end point
                this should typically be `ORIGIN`.
            parent: The parent for the flag
            duration: The beat corresponding to the flag. This controls the flag
                glyph rendered.
            direction: The direction of the flag
        """
        self.duration = duration
        self.direction = direction
        if self.direction == 1:
            glyph_name = self._down_glyphnames[self.duration.base_division]
        else:
            glyph_name = self._up_glyphnames[self.duration.base_division]
        MusicText.__init__(self, pos, parent, [glyph_name])
        StaffObject.__init__(self, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self) -> Beat:
        """The beat corresponding to this flag"""
        return self._duration

    @duration.setter
    def duration(self, value: Beat):
        if not self.needs_flag(value):
            raise NoFlagNeededError(value)
        self._duration = value

    @property
    def direction(self) -> VerticalDirection:
        """The flag direction"""
        return self._direction

    @direction.setter
    def direction(self, value: VerticalDirection):
        self._direction = value

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def needs_flag(cls, duration: Beat) -> bool:
        """Determine if a Beat needs a flag."""
        return duration.base_division in cls._up_glyphnames

    @classmethod
    def vertical_offset_needed(cls, duration: Beat) -> int:
        """Find the space needed in a stem using a flag of a given duration

        Returns: a number to be plugged into a staff unit
        """
        # TODO LOW I believe this should become longer according to
        # division (and thus number of flaglets)
        if cls.needs_flag(duration):
            return 1
        else:
            return 0
