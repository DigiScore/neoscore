from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.layout_controllers import NewLine
from neoscore.core.units import ZERO, Unit
from neoscore.western.staff_fringe_layout import StaffFringeLayout

if TYPE_CHECKING:
    from neoscore.western.abstract_staff import AbstractStaff


class StaffGroup:

    # Fringe padding constants in pseudo-staff-units
    # Padding to the right of the entire fringe
    RIGHT_PADDING = 1
    # Padding to the left of clefs in fringes
    CLEF_LEFT_PADDING = 0.5
    # Padding to the left of time signatures in fringes
    TIME_SIG_LEFT_PADDING = 0.5
    # PAdding to the left of key signatures in fringes
    KEY_SIG_LEFT_PADDING = 0.5

    def __init__(self) -> None:
        self._fringe_layout_cache: dict[
            tuple[AbstractStaff, Optional[NewLine]], StaffFringeLayout
        ] = {}
        self.staves: list[AbstractStaff] = []

    def fringe_layout_at(
        self, staff: AbstractStaff, location: Optional[NewLine]
    ) -> StaffFringeLayout:
        # If the layout is already cached, return it
        cached_value = self._fringe_layout_cache.get((staff, location))
        if cached_value:
            return cached_value
        # Work out the layouts of each staff in isolation first
        isolated_layouts = []
        min_staff_basis = ZERO  # Wider fringes give a lower number here (further left)
        for iter_staff in self.staves:
            layout = iter_staff._fringe_layout_for_isolated_staff(location)
            min_staff_basis = min(min_staff_basis, layout.staff)
            isolated_layouts.append((iter_staff, layout))
        # Then align each layout to fit the widest layout found, and store each in cache
        for iter_staff, isolated_layout in isolated_layouts:
            aligned_layout = self._align_layout(isolated_layout, min_staff_basis)
            self._fringe_layout_cache[(iter_staff, location)] = aligned_layout
        # Now the requested layout is cached, so return it
        return self._fringe_layout_cache[(staff, location)]

    def _align_layout(
        self, layout: StaffFringeLayout, staff_basis: Unit
    ) -> StaffFringeLayout:
        if layout.staff == staff_basis:
            return layout
        # Find the delta from the layout's staff basis to the alignment's
        # Note that these are all *negative* numbers
        delta = staff_basis - layout.staff
        return StaffFringeLayout(
            layout.pos_x_in_staff,
            # Staff, clef, and key signatures are left-aligned to widest fringe
            layout.staff + delta,
            layout.clef + delta,
            layout.key_signature + delta,
            # Time signatures are right-aligned
            layout.time_signature,
        )
