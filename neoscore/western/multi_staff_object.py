from typing import List, Union

from neoscore.core.units import Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.staff_group import StaffGroup


class MultiStaffObject:

    """An object which spans several staves.

    This is a mixin class for :obj:`.PositionedObject` classes. Such
    ``PositionedObject``\ s must have their highest staff also be their parent such that
    ``self.parent == self.highest``.
    """

    def __init__(self, staves: Union[StaffGroup, List[AbstractStaff]]):
        """
        Args:
            staves: The staves this is associated with. If a raw list of staves
                is given, it must be in visually descending order.
        """
        if isinstance(staves, StaffGroup):
            self._staves = staves.staves
        else:
            self._staves = staves

    @property
    def staves(self) -> List[AbstractStaff]:
        """The staves this is associated with, given in descending order."""
        return self._staves

    @staves.setter
    def staves(self, value: List[AbstractStaff]):
        self._staves = value

    @property
    def highest(self) -> AbstractStaff:
        """Shorthand for ``staves[0]``"""
        return self.staves[0]

    @property
    def lowest(self) -> AbstractStaff:
        """Shorthand for ``staves[-1]``"""
        return self.staves[-1]

    @property
    def vertical_span(self) -> Unit:
        """The vertical distance covered by the staves.

        This distance extends from the top line of the top staff to
        the bottom line of the bottom staff.
        """
        highest = self.staves[0]
        lowest = self.staves[-1]
        return highest.unit(highest.map_to(lowest).y + lowest.height)

    @property
    def center_y(self) -> Unit:
        """The vertical center of the staves spanned.

        This value is relative to the top of the highest staff.
        """
        return self.vertical_span / 2
