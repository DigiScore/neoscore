from brown.core.music_text import MusicText
from brown.utils.units import Unit


class Clef(MusicText):

    """A graphical and logical staff clef.

    `Staff`s use these to determine how pitches within them
    should be laid out.
    """

    _canonical_names = {
        'treble': 'gClef',
        'bass': 'fClef',
        '8vb bass': 'fClef8vb',
        'tenor': 'cClef',
        'alto': 'cClef',
    }
    _baseline_staff_positions = {
        'treble': 3,
        'bass': 1,
        '8vb bass': 1,
        'tenor': 1,
        'alto': 2,
    }
    _middle_c_staff_positions = {
        'treble': 5,
        'bass': -1,
        '8vb bass': -6.5,
        'tenor': 1,
        'alto': 2,
    }

    def __init__(self, staff, position_x, clef_type):
        """
        Args:
            staff (Staff):
            position_x (float):
            clef_type (str): One of: 'treble', 'bass', '8vb bass',
                'tenor', or 'alto'
        """
        self._clef_type = clef_type
        # staff_position relies on an existing MusicText object,
        # so start with a temp y position, then set the real one
        MusicText.__init__(self, (position_x, Unit(0)),
                           self._canonical_names[clef_type],
                           staff)
        self.y = self.staff_position

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
        return self.staff.unit(Clef._baseline_staff_positions[self.clef_type])

    @property
    def middle_c_staff_position(self):
        """StaffUnit: The vertical position of middle C for this clef

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.

        This value is primarily useful in calculations of pitch staff positions
        which take a clef into account
        """
        return self.staff.unit(Clef._middle_c_staff_positions[self.clef_type])
