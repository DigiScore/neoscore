from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import BrushDef
from neoscore.core.font import Font
from neoscore.core.layout_controllers import MarginController, NewLine
from neoscore.core.painted_object import PaintedObject
from neoscore.core.pen import PenDef
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.text import Text
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.staff_object import StaffObject


class InstrumentName(PaintedObject, StaffObject):

    """A simple instrument name written in staff fringes

    When created, this causes a given string to be printed in the fringe of each staff
    system. The given position is relative to the top left corner of the staff in the
    fringe, and the text is right-aligned and vertically centered at this point.

    Instrument name changes within a staff are not currently supported.
    """

    def __init__(
        self,
        relative_fringe_pos: PointDef,
        staff: AbstractStaff,
        first_line_text: str,
        later_lines_text: Optional[str] = None,
        font: Optional[Font] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            relative_fringe_pos: The position of the text in the fringe. This is
                relative to the top left corner of the staff in the fringe, and the
                text is right-aligned and vertically centered at this point.
            staff: The parent staff
            first_line_text: The text to write in the first line's fringe
            later_lines_text: Optional different text to write in lines after the first.
                This is useful for writing short-form instrument names. If ``None``, the
                first line text is used everywhere. Set to an empty string to make
                later lines blank.
            font: The font used. Defaults to the document-wide default font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
        """
        StaffObject.__init__(self, staff)
        PaintedObject.__init__(self, ORIGIN, staff, brush, pen)
        if font:
            self._font = font
        else:
            self._font = neoscore.default_font
        self.relative_fringe_pos = relative_fringe_pos
        self._first_line_text = first_line_text
        self._later_lines_text = later_lines_text

    @property
    def relative_fringe_pos(self) -> Point:
        return self._relative_fringe_pos

    @relative_fringe_pos.setter
    def relative_fringe_pos(self, value: PointDef):
        self._relative_fringe_pos = Point.from_def(value)

    @property
    def font(self) -> Font:
        """The text font"""
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value

    @property
    def first_line_text(self) -> str:
        """The text to write in the first line's fringe"""
        return self._first_line_text

    @first_line_text.setter
    def first_line_text(self, value: str):
        self._first_line_text = value

    @property
    def later_lines_text(self) -> Optional[str]:
        """Optional different text to write in lines after the first.

        This is useful for writing short-form instrument names. If ``None``, the first
        line text is used everywhere. Set to an empty string to make later lines blank.
        """
        return self._later_lines_text

    @later_lines_text.setter
    def later_lines_text(self, value: Optional[str]):
        self._later_lines_text = value

    @property
    def _resolved_later_lines_text(self) -> str:
        if self.later_lines_text is None:
            return self.first_line_text
        else:
            return self.later_lines_text

    @property
    def breakable_length(self) -> Unit:
        """This class's breakable length is that of its staff"""
        return self.staff.breakable_length

    @property
    def first_line_visual_width(self) -> Unit:
        """The width of the first line of text"""
        return self.font.bounding_rect_of(self.first_line_text).width

    @property
    def later_lines_visual_width(self) -> Unit:
        """The width of later lines of text"""
        return self.font.bounding_rect_of(self._resolved_later_lines_text).width

    def _render_occurrence(
        self,
        render_call_pos: Point,
        flowable_line: Optional[NewLine],
        is_first_line: bool,
    ):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        pos = Point(
            render_call_pos.x + self.relative_fringe_pos.x + fringe_layout.staff,
            render_call_pos.y + self.relative_fringe_pos.y,
        )
        if is_first_line:
            text = self.first_line_text
        else:
            text = self._resolved_later_lines_text
        if text == "":
            # Skip rendering blank strings
            return
        line_text = Text(
            pos,
            None,
            text,
            self.font,
            self.brush,
            self.pen,
            alignment_x=AlignmentX.RIGHT,
            alignment_y=AlignmentY.CENTER,
        )
        line_text.render()
        line_text.remove()

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        self._render_occurrence(pos, flowable_line, True)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        self._render_occurrence(pos, flowable_line, True)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_occurrence(pos, flowable_line, False)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_occurrence(pos, flowable_line, False)

    def _register_layout_controllers(self):
        # This is known to have some limitations in some cases when a staff is added
        # later in a group than others and has a visually shorted instrument name than
        # the others. See issue #28.
        flowable = self.flowable
        if not flowable:
            return
        staff_flowable_x = flowable.descendant_pos_x(self.staff)
        flowable.add_margin_controller(
            MarginController(
                staff_flowable_x,
                self.first_line_visual_width,
                "_neoscore_instrument_name",
            )
        )
        # Update immediately after for later lines width
        flowable.add_margin_controller(
            MarginController(
                staff_flowable_x + Unit(1),
                self.later_lines_visual_width,
                "_neoscore_instrument_name",
            )
        )

    def pre_render_hook(self):
        super().pre_render_hook()
        self._register_layout_controllers()
