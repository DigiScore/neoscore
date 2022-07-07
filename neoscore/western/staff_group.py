from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sortedcontainers import SortedKeyList  # type: ignore

from neoscore.core import neoscore
from neoscore.core.layout_controllers import NewLine
from neoscore.core.units import ZERO, Unit
from neoscore.western.staff_fringe_layout import StaffFringeLayout

if TYPE_CHECKING:
    from neoscore.western.abstract_staff import AbstractStaff


class StaffGroup:

    """A collection of staves.

    This provides a shared context for staff systems, useful in situations like aligning
    staff fringes.

    Each staff has a reference to a staff group, even if it's a single-item group. See
    :obj:`.AbstractStaff.group`.
    """

    # Fringe padding constants in pseudo-staff-units
    RIGHT_PADDING = 1
    """Padding to the right of all staff fringes, in pseudo-staff-units."""

    CLEF_LEFT_PADDING = 0.5
    """Padding to the left of clefs in fringes, in pseudo-staff-units."""

    TIME_SIG_LEFT_PADDING = 0.5
    """Padding to the left of time signatures in fringes, in pseudo-staff-units."""

    KEY_SIG_LEFT_PADDING = 0.25
    """Padding to the left of key signatures in fringes, in pseudo-staff-units."""

    def __init__(self) -> None:
        self._fringe_layout_cache: Dict[
            Tuple[AbstractStaff, Optional[NewLine]], StaffFringeLayout
        ] = {}
        # Sort staves according to position to some arbitrary known object
        self._staves: SortedKeyList[AbstractStaff] = SortedKeyList(
            key=lambda s: neoscore.document.pages[0].map_to(s).y
        )

    @property
    def staves(self) -> SortedKeyList[AbstractStaff]:
        """The staves contained in this group.

        Staves shouldn't be directly added to this list; instead register a staff with
        the group when the staff is initialized.

        This list is automatically sorted in visually descending order.
        """
        return self._staves

    def fringe_layout_at(
        self, staff: AbstractStaff, location: Optional[NewLine]
    ) -> StaffFringeLayout:
        """Compute to fringe layout needed for a staff at a given location.

        This automatically aligns the returned layout with the fringes of other staves
        in the group.

        Layouts are internally cached so this is fairly efficient.
        """
        # If the layout is already cached, return it
        cached_value = self._fringe_layout_cache.get((staff, location))
        if cached_value:
            return cached_value
        # If the staff doesn't actually exist at the beginning of a line,
        # Do its fringe layout in isolation
        if not self._staff_exists_at(staff, location):
            layout = staff.fringe_layout_for_isolated_staff(location)
            self._fringe_layout_cache[(staff, location)] = layout
            return layout
        # Work out the layouts of each staff in isolation first
        isolated_layouts = []
        min_staff_basis = ZERO  # Wider fringes give a lower number here (further left)
        for iter_staff in self.staves:
            if not self._staff_exists_at(iter_staff, location):
                continue
            layout = iter_staff.fringe_layout_for_isolated_staff(location)
            min_staff_basis = min(min_staff_basis, layout.staff)
            isolated_layouts.append((iter_staff, layout))
        # Then align each layout to fit the widest layout found, and store each in cache
        for iter_staff, isolated_layout in isolated_layouts:
            aligned_layout = self._align_layout(isolated_layout, min_staff_basis)
            self._fringe_layout_cache[(iter_staff, location)] = aligned_layout
        # Now the requested layout is cached, so return it
        return self._fringe_layout_cache[(staff, location)]

    @staticmethod
    def _staff_exists_at(staff: AbstractStaff, location: Optional[NewLine]) -> bool:
        """Check if a staff exists at a given location"""
        if not location:
            # No good way currently to check without a location
            return True
        staff_pos_x = staff.flowable.descendant_pos_x(staff)
        return (staff_pos_x <= location.flowable_x) and (
            staff_pos_x + staff.breakable_length >= location.flowable_x
        )

    @staticmethod
    def _align_layout(
        layout: StaffFringeLayout, staff_basis: Unit
    ) -> StaffFringeLayout:
        if layout.staff == staff_basis:
            return layout
        # Find the delta from the layout's staff basis to the alignment's
        # Note that these are all *negative* numbers
        delta = staff_basis - layout.staff
        return StaffFringeLayout(
            layout.pos_x_in_staff,
            # Staff, clef, and key signatures are left-aligned to the widest fringe
            layout.staff + delta,
            layout.clef + delta,
            layout.key_signature + delta,
            # Time signatures are right-aligned
            layout.time_signature,
        )
