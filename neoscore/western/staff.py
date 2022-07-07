from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, cast

from neoscore.core.exceptions import NoClefError
from neoscore.core.layout_controllers import MarginController, NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.units import ZERO, Mm, Unit, make_unit_class
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.staff_fringe_layout import StaffFringeLayout
from neoscore.western.staff_group import StaffGroup

if TYPE_CHECKING:
    from neoscore.western.clef import Clef
    from neoscore.western.key_signature import KeySignature


class Staff(AbstractStaff):
    """A staff with some high-level knowledge of its contents."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
        group: Optional[StaffGroup] = None,
        line_spacing: Unit = Mm(1.75),
        line_count: int = 5,
        music_font_family: str = "Bravura",
        pen: Optional[PenDef] = None,
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
            music_font_family: The name of the font to use for MusicText objects
                in the staff. This defaults to the system-wide default music font
                family.
            pen: The pen used to draw the staff lines. Defaults to a line with
                thickness from the music font's engraving default.
        """
        unit = self._make_unit_class(line_spacing)
        music_font = MusicFont(music_font_family, unit)
        pen = pen or Pen(thickness=music_font.engraving_defaults["staffLineThickness"])
        super().__init__(
            pos, parent, length, group, unit(1), line_count, music_font, pen
        )

    def distance_to_next_of_type(self, staff_object: PositionedObject) -> Unit:
        """Find the x distance until the next occurrence of an object's type.

        If the object is the last of its type, this gives the remaining length of the
        staff after the object.

        This is useful for determining rendering behavior of staff objects which are
        active until another of their type occurs, such as :obj:`.KeySignature` and
        :obj:`.Clef`.
        """
        start_x = self.map_x_to(cast(PositionedObject, staff_object))
        all_others_of_class = (
            item
            for item in self.descendants_of_exact_class(type(staff_object))
            if item != staff_object
        )
        closest_x = Unit(float("inf"))
        for item in all_others_of_class:
            relative_x = self.map_x_to(item)
            if start_x < relative_x < closest_x:
                closest_x = relative_x
        if closest_x == Unit(float("inf")):
            return self.breakable_length - start_x
        return closest_x - start_x

    @render_cached_property
    def clefs(self) -> List[Tuple[Unit, Clef]]:
        """All the clefs in this staff, ordered by their relative x pos."""
        return self.find_ordered_descendants_with_attr("middle_c_staff_position")

    def active_clef_at(self, pos_x: Unit) -> Optional[Clef]:
        """Return the active clef at a given x position, if any."""
        return next(
            (clef for (clef_x, clef) in reversed(self.clefs) if clef_x <= pos_x),
            None,
        )

    @render_cached_property
    def key_signatures(self) -> List[Tuple[Unit, KeySignature]]:
        """All the key signatures in this staff, ordered by their relative x pos."""
        return self.find_ordered_descendants_with_attr(
            "_neoscore_key_signature_type_marker"
        )

    @render_cached_property
    def time_signatures(self) -> List[Tuple[Unit, KeySignature]]:
        """All the time signatures in this staff, ordered by their relative x pos."""
        return self.find_ordered_descendants_with_attr(
            "_neoscore_time_signature_type_marker"
        )

    def active_key_signature_at(self, pos_x: Unit) -> Optional[KeySignature]:
        """Return the active key signature at a given x position, if any."""
        return next(
            (sig for (sig_x, sig) in reversed(self.key_signatures) if sig_x <= pos_x),
            None,
        )

    def middle_c_at(self, pos_x: Unit) -> Unit:
        """Find the y-axis staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c.

        Raises:
            NoClefError:
                If no clef is active at the given position.
        """
        clef = self.active_clef_at(pos_x)
        if clef is None:
            raise NoClefError
        return clef.middle_c_staff_position

    def y_on_ledger(self, pos_y: Unit) -> bool:
        """Determine if a y-axis position is approximately at a ledger line position

        This is true for any whole-number staff position outside the staff
        """
        return (not self.y_inside_staff(pos_y)) and self.unit(
            pos_y
        ).display_value % 1 == 0

    def ledgers_needed_for_y(self, position: Unit) -> List[Unit]:
        """Find the y positions of all ledgers needed for a given y position"""
        # Work on positions as integers for simplicity
        start = int(self.unit(position).display_value)
        if start < 0:
            return [self.unit(pos) for pos in range(start, 0, 1)]
        elif start > self.line_count - 1:
            return [self.unit(pos) for pos in range(start, self.line_count - 1, -1)]
        else:
            return []

    @staticmethod
    def _make_unit_class(staff_unit_size: Unit) -> Type[Unit]:
        """Create a Unit class with a ratio of 1 to a staff unit size."""
        return make_unit_class("StaffUnit", staff_unit_size.base_value)

    def register_layout_controllers(self):
        # This is known to have some limitations in some cases when staves in a group
        # have different key signatures. See issue #28.
        flowable = self.flowable
        if not flowable:
            return
        staff_flowable_x = flowable.descendant_pos_x(self)
        flowable.add_margin_controller(
            MarginController(
                staff_flowable_x, self.unit(StaffGroup.RIGHT_PADDING), "_neoscore_staff"
            )
        )
        for clef_x, clef in self.clefs:
            flowable_x = staff_flowable_x + clef_x
            margin_needed = clef.bounding_rect.width
            if margin_needed != ZERO:
                # Some clefs can be zero-width; don't add padding in that case.
                margin_needed += self.unit(StaffGroup.CLEF_LEFT_PADDING)
            flowable.add_margin_controller(
                MarginController(flowable_x, margin_needed, "_neoscore_clef")
            )
        # Assume that key signatures have the same width in all clefs
        for key_sig_x, key_sig in self.key_signatures:
            flowable_x = staff_flowable_x + key_sig_x
            flowable.add_margin_controller(
                MarginController(
                    flowable_x,
                    key_sig.visual_width + self.unit(StaffGroup.KEY_SIG_LEFT_PADDING),
                    "_neoscore_key_signature",
                )
            )
        for time_sig in self.descendants_with_attribute(
            "_neoscore_time_signature_type_marker"
        ):
            flowable_x = flowable.descendant_pos_x(time_sig)
            flowable.add_margin_controller(
                MarginController(
                    flowable_x,
                    time_sig.visual_width + self.unit(StaffGroup.TIME_SIG_LEFT_PADDING),
                    "_neoscore_time_signature",
                )
            )
            # Cancel the margin controller immediately after it, this way time
            # signatures only affect margins if they lie right around a line start.
            flowable.add_margin_controller(
                MarginController(flowable_x + Unit(1), ZERO, "_neoscore_time_signature")
            )

    def fringe_layout_for_isolated_staff(
        self, location: Optional[NewLine]
    ) -> StaffFringeLayout:
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
        clef = self.active_clef_at(staff_pos_x)
        key_sig = self.active_key_signature_at(staff_pos_x)
        time_sig = next(
            (sig for x, sig in self.time_signatures if x == staff_pos_x), None
        )
        clef_fringe_pos = current_x
        key_signature_fringe_pos = current_x
        time_signature_fringe_pos = current_x

        if time_sig:
            current_x -= time_sig.visual_width
            time_signature_fringe_pos = current_x
            current_x -= self.unit(StaffGroup.TIME_SIG_LEFT_PADDING)
        if key_sig:
            current_x -= key_sig.visual_width
            key_signature_fringe_pos = current_x
            current_x -= self.unit(StaffGroup.KEY_SIG_LEFT_PADDING)
        if clef:
            clef_width = clef.bounding_rect.width
            current_x -= clef_width
            clef_fringe_pos = current_x
            if clef_width != ZERO:
                # Some clefs can be zero-width (invisible) - don't pad in this case.
                current_x -= self.unit(StaffGroup.CLEF_LEFT_PADDING)
        staff_fringe_pos = current_x
        return StaffFringeLayout(
            staff_pos_x,
            staff_fringe_pos,
            clef_fringe_pos,
            key_signature_fringe_pos,
            time_signature_fringe_pos,
        )
