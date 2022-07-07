from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.layout_controllers import MarginController, NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.units import ZERO, Mm, Unit, make_unit_class
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.staff_fringe_layout import StaffFringeLayout
from neoscore.western.staff_group import StaffGroup

if TYPE_CHECKING:
    from neoscore.western.tab_clef import TabClef

_LINE_SPACE_TO_FONT_UNIT_RATIO: float = 2 / 3


class TabStaff(AbstractStaff):
    """A staff for writing guitar tablature with any number of strings.

    This class is not suitable for use with :obj:`.Chordrest`, :obj:`.Clef`,
    :obj:`.TimeSignature`, and other such classes dependent on classical staff
    semantics.

    While ``TabStaff`` has a :obj:`.MusicFont`, its unit does not necessarily correspond
    to the distance between staff lines. By default, the line spacing is wider than
    classical staves, and its ``MusicFont`` is sized to 2/3 that spacing.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
        group: Optional[StaffGroup] = None,
        line_spacing: Unit = Mm(2.5),
        line_count: int = 6,
        music_font: Optional[MusicFont] = None,
        pen: Optional[Pen] = None,
    ):
        """
        Args:
            pos: The position of the top-left corner of the staff
            parent: The parent for the staff. Make this a :obj:`.Flowable`
                to allow the staff to run across line and page breaks.
            length: The horizontal width of the staff
            group: The staff group this belongs to. Set this if being used in a system
                of multiple staves.
            line_spacing: The distance between two lines in the staff.
            line_count: The number of lines in the staff.
            music_font: The font to use for :obj:`.MusicText` objects in the staff.
                Unlike in :obj:`.Staff`, this font's ``unit`` is not necessarily equivalent
                to the space between two staff (string) lines. By default, this will
                use the system-wide default music font with a unit sized to 2/3 the
                staff line spacing.
            pen: The pen used to draw the staff lines. Defaults to a line with
                thickness from the music font's engraving default.
        """
        music_font = music_font or MusicFont(
            "Bravura",
            make_unit_class(
                "TabStaffTextUnit",
                line_spacing.base_value * _LINE_SPACE_TO_FONT_UNIT_RATIO,
            ),
        )
        pen = pen or Pen(thickness=music_font.engraving_defaults["staffLineThickness"])
        super().__init__(
            pos, parent, length, group, line_spacing, line_count, music_font, pen
        )

    def string_y(self, string: int) -> Unit:
        """Return the Y position of a given string's line.

        Strings are indicated from 1 to N, where 1 is the top string
        and N is the bottom.
        """
        return self.line_spacing * (string - 1)

    @property
    def font_to_staff_space_ratio(self) -> float:
        """Conversion ratio between the font's unit and the staff line spacing."""
        return cast(float, self.unit(1) / self.line_spacing)

    @render_cached_property
    def clefs(self) -> List[Tuple[Unit, TabClef]]:
        """All the clefs in this staff, ordered by their relative x pos."""
        return self.find_ordered_descendants_with_attr("_neoscore_tab_clef_type_marker")

    def active_clef_at(self, pos_x: Unit) -> Optional[TabClef]:
        """Return the active clef at a given x position, if any."""
        return next(
            (clef for (clef_x, clef) in reversed(self.clefs) if clef_x <= pos_x),
            None,
        )

    def register_layout_controllers(self):
        """Register any flowable margin controllers needed by the staff.

        Staff subclasses must implement this.
        """
        flowable = self.flowable
        if not flowable:
            return
        staff_flowable_x = flowable.descendant_pos_x(self)
        flowable.add_margin_controller(
            MarginController(
                staff_flowable_x, self.unit(StaffGroup.RIGHT_PADDING), "neoscore_staff"
            )
        )
        for clef_x, clef in self.clefs:
            flowable_x = staff_flowable_x + clef_x
            margin_needed = clef.bounding_rect.width + self.unit(
                StaffGroup.CLEF_LEFT_PADDING
            )
            flowable.add_margin_controller(
                MarginController(flowable_x, margin_needed, "neoscore_clef")
            )

    def fringe_layout_for_isolated_staff(
        self, location: Optional[NewLine]
    ) -> StaffFringeLayout:
        """Determine the staff fringe layout of this staff in isolation.

        This is the layout needed if this staff was alone in a staff system.
        ``StaffGroup`` uses this as a starting point in its fringe layout logic.

        Staff subclasses must implement this.
        """
        if location:
            staff_pos_x = location.flowable_x - self.flowable.descendant_pos_x(self)
            if staff_pos_x < ZERO:
                # This happens on the first line of a staff positioned at x>0 relative
                # to its flowable.
                staff_pos_x = ZERO
        else:
            staff_pos_x = ZERO
        # Work right-to-left through different fringe layers
        current_x = -self.unit(StaffGroup.RIGHT_PADDING)
        clef_fringe_pos = current_x
        clef = self.active_clef_at(staff_pos_x)
        if clef:
            current_x -= clef.bounding_rect.width
            clef_fringe_pos = current_x
            current_x -= self.unit(StaffGroup.CLEF_LEFT_PADDING)
        staff_fringe_pos = current_x
        return StaffFringeLayout(
            staff_pos_x, staff_fringe_pos, clef_fringe_pos, ZERO, ZERO
        )
