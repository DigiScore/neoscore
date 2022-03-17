from typing import Union

from neoscore.core.music_text import MusicText
from neoscore.models.clef_type import ClefType
from neoscore.utils.units import Unit
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class Clef(MusicText, StaffObject):

    """A graphical and logical staff clef.

    `Clef`s are drawn at the initially specified position, and at the
    beginning of new lines in the parent `Staff` until a new `Clef`
    is encountered or the end of the `Staff`.

    `Staff`s use these to determine how pitches within them should be laid out.
    """

    _canonical_names = {
        ClefType.TREBLE: "gClef",
        ClefType.BASS: "fClef",
        ClefType.BASS_8VB: "fClef8vb",
        ClefType.TENOR: "cClef",
        ClefType.ALTO: "cClef",
    }
    _baseline_staff_positions = {
        ClefType.TREBLE: 3,
        ClefType.BASS: 1,
        ClefType.BASS_8VB: 1,
        ClefType.TENOR: 1,
        ClefType.ALTO: 2,
    }
    _middle_c_staff_positions = {
        ClefType.TREBLE: 5,
        ClefType.BASS: -1,
        ClefType.BASS_8VB: -6.5,
        ClefType.TENOR: 1,
        ClefType.ALTO: 2,
    }

    def __init__(self, pos_x: Unit, staff: Staff, clef_type: Union[ClefType, str]):
        """
        Args:
            pos_x (Unit):
            staff (Staff):
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
            self._clef_type = ClefType[clef_type.upper()]
        MusicText.__init__(
            self, (pos_x, staff.unit(0)), staff, self._canonical_names[self._clef_type]
        )
        StaffObject.__init__(self, staff)
        self.y = self.staff_position

    ######## PUBLIC PROPERTIES ########

    @property
    def clef_type(self):
        """ClefType: The type of clef, both logical and graphical."""
        return self._clef_type

    @property
    def length(self):
        """Find the length in the staff during which this clef is active.

        This is defined as the distance relative to the staff until
        the next clef is encountered. If no further clefs are found,
        this is the remaining length of the staff.
        """
        # Iterate through the (typically cached) staff clef list
        # The list is sorted by x position relative to the staff,
        # which means the first loop pass in which self_staff_x
        # has been assigned must be the next clef in the staff.
        self_staff_x = None
        for (staff_x, clef) in self.staff.clefs():
            if self_staff_x is not None:
                return staff_x - self_staff_x
            if clef is self:
                self_staff_x = staff_x
        # No later clefs exist; return the remaining staff length
        return self.staff.length - self_staff_x

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

    ######## PRIVATE METHODS ########

    # Always render the whole glyph.

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self._render_slice(start, None)

    def _render_after_break(self, local_start_x, start):
        self._render_slice(start, None)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_slice(start, None)
