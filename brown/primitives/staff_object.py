from abc import ABC

# from brown.core import FlowableObject
# from brown.core import Flowable

from brown.utils import units

# from brown.models.duration import Duration
from brown.models.position import Position

from brown.primitives.staff import Staff



# what about spanners?


class StaffObject:

    """An object in a staff """

    def __init__(self, staff, position):
        '''
        Args:
            staff (Staff): The parent staff
            position (Position): The position of the object
        '''
        self.staff = staff
        self.position = position

    @property
    def staff(self):
        return self._staff

    @staff.setter
    def staff(self, value):
        self._staff = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
