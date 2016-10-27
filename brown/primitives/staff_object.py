from abc import ABC

# from brown.core import FlowableObject
# from brown.core import Flowable

from brown.utils import units
# from brown.models.duration import Duration


# what about spanners?

class NoAncestorStaffError(Exception):
    """Exception raised when no ancestor of a StaffObject is a Staff."""
    pass


class StaffObject(ABC):

    """An object in a staff """

    def __init__(self, parent, position_x):
        '''
        Args:
            staff (Staff): The parent staff
            position_x (float): The x-position of the object in staff-units
        '''
        self._parent = parent
        self.root_staff._register_staff_object(self)
        self._position_x = position_x
        self._grob = None

    ######## PUBLIC PROPERTIES ########

    @property
    def grob(self):
        """The core graphical object representation of this StaffObject

        This value is read-only.
        """
        return self._grob

    @property
    def root_staff(self):
        """The staff associated with this object"""
        # TODO: Maybe just fold the logic directly into here
        return self._find_ancestor_staff()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if self._grob is not None and self._parent is not None:
            self.grob.parent = self._parent.grob

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        self._position_x = value
        # TODO: This may not be the best way to handle propagating changed
        #       to grob, and it is not consistently implemented in similar
        #       classes.
        self.grob.x = value

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

        # TODO: out of date?

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        raise NotImplementedError

    @position_y.setter
    def position_y(self, value):
        raise NotImplementedError

    @property
    def position_y_in_staff_units(self):
        """float: The y position in staff units below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        raise NotImplementedError

    @position_y.setter
    def position_y_in_staff_units(self, value):
        raise NotImplementedError

    ######## PUBLIC METHODS ########

    def render(self):
        raise NotImplementedError

    ######## PRIVATE METHODS ########

    def _find_ancestor_staff(self):
        """Traverse the parent chain until a `Staff` is found, and return it.

        This is used when looking up the root staff for StaffObjects.

        Returns: Staff

        Raises: NoAncestorStaffError if no such `Staff` exists.
        """
        try:
            ancestor = self.parent
            while type(ancestor).__name__ != 'Staff':
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            raise NoAncestorStaffError
