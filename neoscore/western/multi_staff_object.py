from collections.abc import Iterable

from neoscore.core import mapping
from neoscore.utils.units import Unit
from neoscore.western.staff import Staff


class MultiStaffObject:

    """An object which spans several staves.

    This is a Mixin class, meant to be combined with PositionedObject classes.

    `MultiStaffObject`s must have their visually highest staff as their parent.

    If an class is both a `MultiStaffObject` and a `StaffObject`,
    the parent staff should be the visually highest staff listed in
    `self.staves`.
    """

    def __init__(self, staves: Staff | Iterable[Staff]):
        """
        Args:
            staves: The staves this is associated with.
        """
        self.staves = set(staves) if isinstance(staves, Iterable) else {staves}

    ######## PUBLIC PROPERTIES ########

    @property
    def visually_sorted_staves(self) -> list[Staff]:
        """`self.staves` as a list in visually descending order"""
        # TODO MEDIUM this assumes that all staves have the same parent
        return sorted(list(self.staves), key=lambda s: s.y)

    @property
    def highest_staff(self) -> Staff:
        """The visually highest staff in self.staves"""
        return self.visually_sorted_staves[0]

    @property
    def lowest_staff(self) -> Staff:
        """The visually lowest staff in self.staves"""
        return self.visually_sorted_staves[-1]

    @property
    def vertical_span(self) -> Unit:
        """The vertical distance covered by the staves

        The distance from the top of `self.highest_staff` to the bottom
        of `self.lowest_staff`, in `self.highest_staff.unit` StaffUnits.
        """
        return self.highest_staff.unit(
            mapping.map_between(self.highest_staff, self.lowest_staff).y
            + self.lowest_staff.height
        )
