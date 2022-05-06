from neoscore.core.units import Unit
from neoscore.western.abstract_staff import AbstractStaff


class MultiStaffObject:

    """An object which spans several staves.

    This is a Mixin class, meant to be combined with PositionedObject classes.

    These must have their visually highest staff as their parent.
    """

    def __init__(self, staves: list[AbstractStaff]):
        """
        Args:
            staves: The staves this is associated with, given in descending order.
        """
        # TODO HIGH make this a StaffGroup instead - and update StaffGroup to use a sorted list
        self._staves = staves

    ######## PUBLIC PROPERTIES ########

    @property
    def staves(self) -> list[AbstractStaff]:
        """The staves this is associated with, given in descending order."""
        return self._staves

    @staves.setter
    def staves(self, value: list[AbstractStaff]):
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
