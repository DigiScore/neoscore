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
            parent_staff (Staff):
            position_x (float):
            pitch (Pitch):
        """
        super(Notehead, self).__init__(staff, position_x)
        self.pitch = pitch
        self.grob = Glyph(
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
    def position_relative_to_middle_c(self):
        middle_c = (4 * 7) + 1
        note_pos = (self.pitch.octave * 7) + self.pitch.diatonic_degree_in_c
        return note_pos - middle_c

    @property
    def staff_position(self):
        """int: The notehead position in the staff in staff units

        0 means the center
        line or space of the staff, higher numbers mean higher pitches,
        and lower numbers mean lower pitches.
        """
        return (self.staff.middle_c_at(self.position_x)
                + self.position_relative_to_middle_c)

    @property
    def position_relative_to_top(self):
        """int: The vertical staff position of this notehead relative to
        the top of the staff. Lower numbers mean visually lower positions,
        and higher numbers mean visually higher positions."""
        return(self.staff.middle_c_at(self.position_x))

    @property
    def position_y(self):
        """float: The vertical staff position of the notehead in pixels
        relative to the top of the staff."""
        position_relative_to_top = (-1 * self.staff_position) + 4
        # Convert to pixels and return
        return (position_relative_to_top) * (self.staff.staff_unit / 2)

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
