from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.core import brown


class Accidental(StaffObject):

    _smufl_codepoints = {
        -2: '\uE264',  # Double-Flat
        -1: '\uE260',  # Flat
        0:  '\uE261',  # Natural
        1:  '\uE262',  # Sharp
        2:  '\uE263',  # Double-Sharp
    }

    def __init__(self, notehead, x_offset):
        """
        Args:
            notehead (Notehead): The parent Notehead object
            x_offset (float): The x offset (in pixels) from the notehead
        """
        self._notehead = notehead
        self._x_offset = x_offset
        super(Accidental, self).__init__(self.notehead.staff,
                                         self.notehead.position_x + self.x_offset)
        if self.virtual_accidental.value is not None:
            self._grob = Glyph(
                self.staff.x + self.position_x,  # TODO: We should be able to pass relative coords
                self.staff.y + self.position_y,
                Accidental._smufl_codepoints[self.virtual_accidental.value],
                brown.music_font)
            self.grob.position_y_baseline(self.staff.y + self.position_y)
            self.grob_width = 1.25 * self.staff.staff_unit  # TODO: Temporary testing
        else:
            self._grob = None
            self.grob_width = 0

    ######## PUBLIC PROPERTIES ########

    @property
    def virtual_accidental(self):
        """VirtualAccidental: What type of accidental this is.

        This property is read-only. To change the accidental,
        modify `self.notehead.pitch`.
        """
        return self.notehead.pitch.virtual_accidental

    @property
    def staff_position(self):
        """int: The notehead position in the staff in staff units

        0 means the center line or space of the staff, higher numbers
        mean higher pitches, and lower numbers mean lower pitches.
        """
        return self.notehead.staff_position

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        return self.staff._staff_pos_to_rel_pixels(self.staff_position)

    @property
    def notehead(self):
        """Notehead: The parent Notehead."""
        return self._notehead

    @property
    def x_offset(self):
        """float: The x offset (in pixels) from the parent notehead"""
        return self._x_offset

    ######## PUBLIC METHODS ########

    def render(self):
        # Only draw if a grob exists
        if self.grob is not None:
            self.grob.render()
