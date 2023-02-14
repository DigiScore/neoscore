from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import Point
from neoscore.core.positioned_object import render_cached_property
from neoscore.core.units import ZERO, Unit
from neoscore.western.clef_type import ClefType, ClefTypeDef
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class Clef(MusicText, StaffObject):

    """A graphical and logical staff clef.

    These are drawn at the initially specified position, and at the beginning of new
    lines in the parent :obj:`.Staff` until a new ``Clef`` is encountered or the end of
    the ``Staff``.

    ``Staff`` uses these to map pitches to vertical positions.
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
                given as a convenience; see :obj:`.ClefTypeDef`.
            font: The font used. Defaults to the staff's font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
        """
        StaffObject.__init__(self, staff)
        # Init with placeholder y position and text; clef_type setter will update
        MusicText.__init__(self, (pos_x, ZERO), staff, "", font, brush, pen)
        self.clef_type = clef_type

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

    @render_cached_property
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
        for staff_x, clef in self.staff.clefs:
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

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        if fringe_layout.pos_x_in_staff == self.pos_x_in_staff:
            pos = Point(pos.x + fringe_layout.clef, pos.y)
        super().render_complete(pos, flowable_line)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        if fringe_layout.pos_x_in_staff == self.pos_x_in_staff:
            pos = Point(pos.x + fringe_layout.clef, pos.y)
        super().render_complete(pos, flowable_line)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.clef, pos.y), flowable_line)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.clef, pos.y), flowable_line)
