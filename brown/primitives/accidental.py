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

    def __init__(self, notehead, position_x):
        """
        Args:
            notehead (Notehead): The parent Notehead object
            position_x (float): The x position (in pixels) relative to the notehead
        """
        self._notehead = notehead
        super().__init__(self.notehead, position_x)
        if self.virtual_accidental.value is not None:
            self._grob = Glyph(
                self.position_x,
                0,
                Accidental._smufl_codepoints[self.virtual_accidental.value],
                brown.music_font,
                self.parent.grob)
            # TODO: Baseline offset has already been performed by parent object,
            #       how can positioning be handled correctly with a parentage system?
            #self.grob.position_y_baseline(0)
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
    def notehead(self):
        """Notehead: The parent Notehead."""
        return self._notehead

    ######## PUBLIC METHODS ########

    def render(self):
        # Only draw if a grob exists
        if self.grob is not None:
            self.grob.render()
