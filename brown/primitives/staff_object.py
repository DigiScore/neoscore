from abc import ABC

# from brown.core import FlowableObject
# from brown.core import Flowable

from brown.utils import units

# from brown.models.duration import Duration

from brown.primitives.staff import Staff



# what about spanners?


class StaffObject(ABC):

    """An object in a staff """

    def __init__(self, staff, position_x):
        '''
        Args:
            staff (Staff): The parent staff
            position_x (float): The x-position of the object in staff-units
        '''
        self.staff = staff
        self.position_x = position_x

    ######## PUBLIC PROPERTIES ########

    @property
    def staff(self):
        return self._staff

    @staff.setter
    def staff(self, value):
        self._staff = value

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        self._position_x = value

    @property
    def position_y(self):
        """float: The y position in pixels below top of the staff.

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
