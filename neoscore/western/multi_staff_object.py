from typing import TypeAlias, Union

from neoscore.core import mapping
from neoscore.core.units import Unit
from neoscore.western.staff import Staff
from neoscore.western.tab_staff import TabStaff

StaffLike: TypeAlias = Union[Staff, TabStaff]


class MultiStaffObject:

    """An object which spans several staves.

    This is a Mixin class, meant to be combined with PositionedObject classes.

    `MultiStaffObject`s must have their visually highest staff as their parent.
    """

    def __init__(self, staves: list[StaffLike]):
        """
        Args:
            staves: The staves this is associated with, given in descending order.
        """
        self._staves = staves

    ######## PUBLIC PROPERTIES ########

    @property
    def staves(self) -> list[StaffLike]:
        """The staves this is associated with, given in descending order."""
        return self._staves

    @staves.setter
    def staves(self, value: list[StaffLike]):
        self._staves = value

    @property
    def highest(self) -> StaffLike:
        """Shorthand for `staves[0]`"""
        return self.staves[0]

    @property
    def lowest(self) -> StaffLike:
        """Shorthand for `staves[-1]`"""
        return self.staves[-1]

    @property
    def vertical_span(self) -> Unit:
        """The vertical distance covered by the staves.

        This distance extends from the top line of the top staff to
        the bottom line of the bottom staff.
        """
        highest = self.staves[0]
        lowest = self.staves[-1]
        return highest.unit(mapping.map_between(highest, lowest).y + lowest.height)
