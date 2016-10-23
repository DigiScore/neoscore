from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff_object import StaffObject
from brown.models.pitch import Pitch
from brown.core import brown


class Clef(StaffObject):

    _baseline_staff_positions = {
        'treble': 6,    # Treble clef baseline is middle of the G curl
        'bass': 2,      # Bass clef baseline is between the two dots
        '8vb bass': 2,  # 8vb Bass clef baseline same as regular bass clef
        'tenor': 2,     # C clef baseline is in the middle of the glyph
        'alto': 4,
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
    # TODO: unify staff position systems -
    #       notice how _baseline_staff_positions and _middle_c_staff_positions
    #       are actually in different coordinate systems

    def __init__(self, staff, position_x, clef_type):
        """
        Args:
            parent_staff (Staff):
            position_x (float):
            pitch (Pitch):
        """
        super(Clef, self).__init__(staff, position_x)
        self._clef_type = clef_type
        self.grob = Glyph(
            self.staff.x + self.position_x,  # TODO: pass relative coords
            self.staff.y + self.position_y,
            Clef._smufl_codepoints[self.clef_type],
            brown.music_font)
        self.grob.position_y_baseline(self.staff.y + self.position_y)

    ######## PUBLIC PROPERTIES ########

    @property
    def clef_type(self):
        """str: The type of clef (e.g. 'treble', 'bass').

        Currently supported types are: `'treble'` and `'bass'`
        """
        return self._clef_type

    @property
    def position_y_in_staff_units(self):
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
        # Take position_y_in_staff_units and convert to pixels
        return self.position_y_in_staff_units * (self.staff.staff_unit / 2)

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
    def natural_midi_number_at_top_staff_line(self):
        """int: The natural midi number of the top staff line for this clef."""
        return Clef._natural_midi_numbers_at_top_staff_line[self.clef_type]

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
