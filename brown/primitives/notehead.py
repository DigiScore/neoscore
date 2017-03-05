from brown.core.music_text import MusicText
from brown.models.pitch import Pitch
from brown.utils.point import Point
from brown.utils.units import Mm


class Notehead(MusicText):

    """A simple Notehead glyph whose appearance is determined by a Duration

    Currently, values larger than whole notes are not supported.
    """

    _glyphnames = {
        1024: 'noteheadBlack',
        512: 'noteheadBlack',
        256: 'noteheadBlack',
        128: 'noteheadBlack',
        64: 'noteheadBlack',
        32: 'noteheadBlack',
        16: 'noteheadBlack',
        8: 'noteheadBlack',
        4: 'noteheadBlack',
        2: 'noteheadHalf',
        1: 'noteheadWhole',
    }

    def __init__(self, position_x, pitch, duration, parent):
        """
        Args:
            staff (Staff)
            position_x (Unit):
            duration (Beat or Beat tuple):
            pitch (Pitch):
        """
        self.pitch = pitch
        self.duration = duration
        # HACK: init pos to temporary position, then set for real
        super().__init__((position_x, Mm(0)),
                         [self._glyphnames[self.duration.base_division]],
                         parent)
        self.pos = Point(position_x, self.staff_position)

    ######## PUBLIC PROPERTIES ########

    @property
    def visual_width(self):
        """Unit: The width of the Notehead"""
        return self.staff.unit(self._bounding_rect.width)

    @property
    def pitch(self):
        """Pitch: The pitch of this notehead.

        May be set to a valid string pitch descriptor.
        See Pitch docs.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        if isinstance(value, Pitch):
            self._pitch = value
        else:
            self._pitch = Pitch(value)

    @property
    def duration(self):
        """Beat: The time duration of this Notehead"""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def staff_position(self):
        """StaffUnit: The notehead position in the staff.

        StaffUnit(0) means the top staff line, higher values
        mean lower pitches, and vice versa.
        """
        return (self.staff.middle_c_at(self.map_to_staff_unflowed().x) +
                self.staff.unit(self.pitch.staff_position_relative_to_middle_c))
