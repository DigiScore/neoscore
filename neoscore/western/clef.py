from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.utils.point import Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western.clef_type import ClefType, ClefTypeDef
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class Clef(MusicText, StaffObject):

    """A graphical and logical staff clef.

    `Clef`s are drawn at the initially specified position, and at the
    beginning of new lines in the parent `Staff` until a new `Clef`
    is encountered or the end of the `Staff`.

    `Staff`s use these to determine how pitches within them should be laid out.
    """

    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        clef_type: ClefTypeDef,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos_x: The x position in the staff
            staff: The parent staff
            clef_type: The type of clef. String names of common clefs may be
                given as a convenience; see `ClefTypeDef`.
        """
        StaffObject.__init__(self, staff)
        # Init with placeholder y position and text; clef_type setter will update
        MusicText.__init__(self, (pos_x, ZERO), staff, "", font, brush, pen)
        self.clef_type = clef_type

    ######## PUBLIC PROPERTIES ########

    @property
    def clef_type(self) -> ClefType:
        """The type of clef, both logical and graphical."""
        return self._clef_type

    @clef_type.setter
    def clef_type(self, value: ClefTypeDef):
        self._clef_type = ClefType.from_def(value)
        if callable(self._clef_type.staff_pos):
            staff_pos = self._clef_type.staff_pos(self.staff.line_count)
        else:
            staff_pos = self._clef_type.staff_pos
        self.y = self.staff.unit(staff_pos)
        self.text = self._clef_type.glyph_name
        if callable(self.clef_type.middle_c_staff_pos):
            middle_c_staff_pos = self.clef_type.middle_c_staff_pos(
                self.staff.line_count
            )
        else:
            middle_c_staff_pos = self.clef_type.middle_c_staff_pos
        self._middle_c_staff_position = self.staff.unit(middle_c_staff_pos)

    @property
    def breakable_length(self) -> Unit:
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
        return self.staff.breakable_length - self_staff_x

    @property
    def middle_c_staff_position(self) -> Unit:
        """The vertical position of middle C for this clef

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.

        This value is primarily useful in calculations of pitch staff positions
        which take a clef into account
        """
        return self._middle_c_staff_position

    ######## PRIVATE METHODS ########

    # Always render the whole glyph.

    def _render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        self._render_slice(start, None)

    def _render_after_break(self, local_start_x: Unit, start: Point):
        self._render_slice(start, None)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_slice(start, None)
