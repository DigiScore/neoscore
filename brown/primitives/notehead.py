from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.core import brown
# from brown.primitives.chord_rest import ChordRest

"""
Thoughts on the Notehead class

* Does not know what part of a chord it is in (is not aware of its context)
* Does have an accidental


"""

class Notehead(StaffObject):

    def __init__(self, staff, position_x, pitch):
        """
        Args:
            staff (Staff):
            position_x (float):
            pitch (Pitch):
        """
        super(Notehead, self).__init__(staff, position_x)
        self.pitch = pitch
        self._grob = Glyph(
            self.staff.x + self.position_x,  # TODO: We should be able to pass relative coords
            self.staff.y + self.position_y,
            '\uE0A4', brown.music_font)
        self.grob.position_y_baseline(self.staff.y + self.position_y)

    ######## PUBLIC PROPERTIES ########

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
        """int: The notehead position in the staff in staff units

        0 means the center
        line or space of the staff, higher numbers mean higher pitches,
        and lower numbers mean lower pitches.
        """
        return (self.staff.middle_c_at(self.position_x) +
                self.pitch.staff_position_relative_to_middle_c)

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        # Take position_y_in_staff_units and convert to pixels
        return (self.staff._centered_position_to_top_down(self.staff_position) *
                (self.staff.staff_unit / 2))

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
