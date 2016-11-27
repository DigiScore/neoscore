from brown.core.flowable_object import FlowableObject
from brown.utils.units import Mm
from brown.utils.point import Point


class NoAncestorStaffError(Exception):
    """Exception raised when no ancestor of a StaffObject is a Staff."""
    pass


class StaffObject(FlowableObject):

    """An object in a staff """

    def __init__(self, pos, breakable_width, parent):
        """
        Args:
            TODO: Docs!
        """
        super().__init__(pos, breakable_width, parent)
        self._parent = parent
        self.root_staff._register_staff_object(self)

    ######## PUBLIC PROPERTIES ########

    @property
    def root_staff(self):
        # TODO: Rename to just `staff` later
        """The staff associated with this object"""
        try:
            ancestor = self.parent
            while type(ancestor).__name__ != 'Staff':
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            raise NoAncestorStaffError

    @property
    def position_y_in_staff_units(self):
        """float: The y position in staff units below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        raise NotImplementedError

    @position_y_in_staff_units.setter
    def position_y_in_staff_units(self, value):
        raise NotImplementedError
