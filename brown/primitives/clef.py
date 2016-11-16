from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff_object import StaffObject
from brown.models.pitch import Pitch
from brown.core import brown


class Clef(StaffObject):

    _baseline_staff_positions = {
        'treble': -2,    # Treble clef baseline is middle of the G curl
        'bass': 2,      # Bass clef baseline is between the two dots
        '8vb bass': 2,  # 8vb Bass clef baseline same as regular bass clef
        'tenor': 2,     # C clef baseline is in the middle of the glyph
        'alto': 0,
    }
    _smufl_codepoints = {
        'treble': '\uE050',
        'bass': '\uE062',
        '8vb bass': '\uE064',
        'tenor': '\uE05C',
        'alto': '\uE05C',
    }
    _middle_c_staff_positions = {
        'treble': -6,
        'bass': 6,
        '8vb bass': 13,
        'tenor': 2,
        'alto': 0,
    }
    _natural_midi_numbers_at_top_staff_line = {
        'treble': 77,
        'bass': 57,
        '8vb bass': 45,
        'tenor': 64,
        'alto': 67
    }

    def __init__(self, parent, position_x, clef_type):
        """
        Args:
            parent (Staff or StaffObject):
            position_x (float):
            pitch (Pitch):
        """
        super().__init__(parent, position_x)
        self._clef_type = clef_type
        self._grob = Glyph(
            (self.position_x, self.position_y),
            Clef._smufl_codepoints[self.clef_type],
            brown.music_font,
            self.parent.grob)
        self.grob.position_y_baseline(self.position_y)

    ######## PUBLIC PROPERTIES ########

    @property
    def clef_type(self):
        """str: The type of clef (e.g. 'treble', 'bass').

        Currently supported types are: `'treble'` and `'bass'`
        """
        return self._clef_type

    @property
    def staff_position(self):
        """float: The y position in staff units below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        return Clef._baseline_staff_positions[self.clef_type]

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        # Take staff_position and convert to pixels
        return self.root_staff._staff_pos_to_rel_pixels(
            self.staff_position)

    @property
    def middle_c_staff_position(self):
        """int: The staff position of middle c for this clef

        This value is a vertical staff position, where 0 means the center
        line or space of the staff, higher numbers mean higher positions,
        and lower numbers mean lower positions.

        This value is primarily useful in calculations of pitch staff positions
        which take a clef into account
        """
        return Clef._middle_c_staff_positions[self.clef_type]

    @property
    def _natural_midi_number_at_top_staff_line(self):
        """int: The natural midi number of the top staff line for this clef."""
        return Clef._natural_midi_numbers_at_top_staff_line[self.clef_type]

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
