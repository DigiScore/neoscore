from brown.core.music_text_object import MusicTextObject


class Clef(MusicTextObject):

    _canonical_names = {
        'treble': 'gClef',
        'bass': 'fClef',
        '8vb bass': 'fClef8vb',
        'tenor': 'cClef',
        'alto': 'cClef',
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
            clef_type (str): One of: 'treble', 'bass', '8vb bass',
                'tenor', or 'alto'
        """
        self._baseline_staff_positions = {
            'treble': staff.unit(3),
            'bass': staff.unit(1),
            '8vb bass': staff.unit(1),
            'tenor': staff.unit(1),
            'alto': staff.unit(2),
        }
        self._middle_c_staff_positions = {
            'treble': staff.unit(5),
            'bass': staff.unit(-1),
            '8vb bass': staff.unit(-6.5),
            'tenor': staff.unit(1),
            'alto': staff.unit(2),
        }
        self._clef_type = clef_type
        MusicTextObject.__init__(self, (position_x, self.staff_position),
                                 [self._canonical_names[clef_type]],
                                 staff)

    ######## PUBLIC PROPERTIES ########

    @property
    def clef_type(self):
        """str: The type of clef (e.g. 'treble', 'bass').

        Currently supported types are: `'treble'` and `'bass'`
        """
        return self._clef_type

    @property
    def staff_position(self):
        """StaffUnit: The y position in staff units below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        return self._baseline_staff_positions[self.clef_type]

    @property
    def middle_c_staff_position(self):
        """StaffUnit: The vertical position of middle C for this clef

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.

        This value is primarily useful in calculations of pitch staff positions
        which take a clef into account
        """
        return self._middle_c_staff_positions[self.clef_type]

    @property
    def _natural_midi_number_at_top_staff_line(self):
        """int: The natural midi number of the top staff line for this clef."""
        return self._natural_midi_numbers_at_top_staff_line[self.clef_type]
