from brown.models.pitch import Pitch
from brown.utils.point import Point
from brown.utils.units import Mm
from brown.core.music_glyph import MusicGlyph


class Notehead(MusicGlyph):

    def __init__(self, position_x, pitch, parent=None):
        """
        Args:
            staff (Staff)
            position_x (Unit):
            pitch (Pitch):
        """
        self.pitch = pitch
        # HACK: init pos to 0, 0, then set for real
        super().__init__((position_x, Mm(0)),
                         'noteheadBlack', parent=parent)
        self.pos = Point(position_x, self.staff_position)

    ######## PUBLIC PROPERTIES ########

    @property
    def visual_width(self):
        """Unit: The width of the Notehead"""
        return self.staff.unit(self.bounding_rect.width)

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
    def staff_position(self):
        """StaffUnit: The notehead position in the staff.

        StaffUnit(0) means the top staff line, higher values
        mean lower pitches, and vice versa.
        """
        return (self.staff.middle_c_at(self.map_between_items(self.staff, self).x) -
                self.staff.unit(self.pitch.staff_position_relative_to_middle_c))
