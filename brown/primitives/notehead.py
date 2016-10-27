from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.core import brown
from brown.primitives.accidental import Accidental
# from brown.primitives.chord_rest import ChordRest

"""
Thoughts on the Notehead class

* Does not know what part of a chord it is in (is not aware of its context)
* Does have an accidental


"""

class Notehead(StaffObject):

    def __init__(self, parent, position_x, pitch):
        """
        Args:
            parent (Staff or StaffObject):
            position_x (float):
            pitch (Pitch):
        """
        super().__init__(parent, position_x)
        self.grob_width = 1.25 * self.root_staff.staff_unit  # TODO: Temporary testing
        self.pitch = pitch
        self._grob = Glyph(
            self.position_x,
            self.position_y,
            '\uE0A4',
            brown.music_font,
            self.parent.grob)
        self.pitch = pitch  # HACK - pitch setter expects self.grob to exist,
                            #        but self.grob setter expects pitch to exist
        self.grob.position_y_baseline(self.position_y)
        self._build_accidental()

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

        0 means the center line or space of the staff, higher numbers
        mean higher pitches, and lower numbers mean lower pitches.
        """
        if self.parent == self.staff:
            pos_x_from_staff = self.position_x
        else:
            pos_x_from_staff = self.position_x + self.parent.position_x
        # HACK: There should be a general way to calculate relative positions
        #       between objects
        return (self.root_staff.middle_c_at(pos_x_from_staff) +
                self.pitch.staff_position_relative_to_middle_c)

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        return self.root_staff._staff_pos_to_rel_pixels(self.staff_position)

    @property
    def position_x(self):
        return self._position_x

    # HACK : Override of staff_object version to propogate changes to child
    #        accidental. Remove once proper parent-child relative position
    #        is implemented.
    @position_x.setter
    def position_x(self, value):
        # TODO: Is there a way in python to call the super class setter?
        self._position_x = value
        self.grob.x = value
        if self.accidental.grob is not None:
            self.accidental.position_x = value

    @property
    def accidental(self):
        """Accidental: The Accidental object for the notehead"""
        return self._accidental

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
        # Render the accidental
        self.accidental.render()

    def _build_accidental(self):
        self._accidental = Accidental(self, self.grob_width * -1)
