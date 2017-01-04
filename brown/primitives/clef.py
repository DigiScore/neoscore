from brown.core.music_glyph import MusicGlyph
from brown.primitives.staff_object import StaffObject
from brown.core import brown


class Clef(MusicGlyph):

    _baseline_staff_positions = {
        'treble': 6,    # Treble clef baseline is middle of the G curl
        'bass': 2,      # Bass clef baseline is between the two dots
        '8vb bass': 2,  # 8vb Bass clef baseline same as regular bass clef
        'tenor': 2,     # C clef baseline is in the middle of the glyph
        'alto': 4,
    }  # (Later when SMuFL impl is better this may not be needed)
    _canonical_names = {
        'treble': 'gClef',
        'bass': 'fClef',
        '8vb bass': 'fClef8vb',
        'tenor': 'cClef',
        'alto': 'cClef',
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

    def __init__(self, staff, position_x, clef_type):
        """
        Args:
            staff (Staff):
            position_x (float):
            pitch (Pitch):
        """
        staff_pos_y = self._baseline_staff_positions[clef_type]  # currently wrong
        MusicGlyph.__init__(self, (position_x, staff.unit(staff_pos_y)),
                            self._canonical_names[clef_type],
                            brown.music_font,
                            staff)
        self._clef_type = clef_type
        #self.position_y_baseline(staff_pos_y)

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
        # TODO: Rework this
        return Clef._baseline_staff_positions[self.clef_type]

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
