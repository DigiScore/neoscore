from brown.core.music_text import MusicText
from brown.models.clef_type import ClefType


class Clef(MusicText):

    """A graphical and logical staff clef.

    `Staff`s use these to determine how pitches within them
    should be laid out.
    """

    _canonical_names = {
        ClefType.treble: 'gClef',
        ClefType.bass: 'fClef',
        ClefType.bass_8vb: 'fClef8vb',
        ClefType.tenor: 'cClef',
        ClefType.alto: 'cClef',
    }
    _baseline_staff_positions = {
        ClefType.treble: 3,
        ClefType.bass: 1,
        ClefType.bass_8vb: 1,
        ClefType.tenor: 1,
        ClefType.alto: 2,
    }
    _middle_c_staff_positions = {
        ClefType.treble: 5,
        ClefType.bass: -1,
        ClefType.bass_8vb: -6.5,
        ClefType.tenor: 1,
        ClefType.alto: 2,
    }

    def __init__(self, staff, position_x, clef_type):
        """
        Args:
            staff (Staff):
            position_x (Unit):
            clef_type (ClefType or str): The type of clef.
                For convenience, any `str` of a `ClefType`
                enum name may be passed.

        Raises:
            KeyError: If the given `clef_type` is not a valid
                `ClefType` or `ClefType` enum name.
        """
        if isinstance(clef_type, ClefType):
            self._clef_type = clef_type
        else:
            self._clef_type = ClefType[clef_type]
        MusicText.__init__(self, (position_x, 0),
                           self._canonical_names[self._clef_type],
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
