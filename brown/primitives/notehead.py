from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
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
            self.staff.x + self.position_x,
            0,
            '\uE13E', Font('gonville', 20))

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
        """int: The notehead position in the staff in staff units.

        0 means the center
        line or space of the staff, higher numbers mean higher pitches,
        and lower numbers mean lower pitches.
        """
        return (self.staff.middle_c_at(self.position_x) +  # Middle c in staff
                (self.pitch.diatonic_degree_from_c - 1) +  # Diatonic pitch number, off by one
                (self.pitch.octave * 8) -                  # Octave multiplier
                (32))                                      # Octave baseline
                                                           # (middle c is octave 4)

    @property
    def position_y(self):
        """The vertical staff position of the notehead"""
        #return staff.
        pass

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
