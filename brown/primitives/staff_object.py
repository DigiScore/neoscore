from brown.core import FlowableObject
from brown.core import Flowable

from brown.utils import units

from brown.models.clef import Clef
from brown.models.duration import Duration
from brown.models.position import Position

from brown.primitives.staff import Staff



# what about spanners?




class StaffObject(FlowableObject):
    def __init__(staff, position, duration=None):
        '''
        Args:
            staff (Staff): The parent staff
            position (Position): The position of the object
            duration (Duration): An optional duration for the object
        '''
        self.staff = staff
        self.position = position
        self.duration = duration


    @property
    def staff():
        return self._staff

    @staff.setter
    def staff(value):
        self._staff = value

    @property
    def position():
        return self._position

    @position.setter
    def position(value):
        self._position = value

    @property
    def duration():
        return self._duration

    @duration.setter
    def duration(value):
        self._duration = value
