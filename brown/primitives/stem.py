from brown.core import brown
from brown.config import config
from brown.core.path import Path
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.utils import units



class Stem(StaffObject):

    def __init__(self, staff, position_x,
                 staff_position_start, staff_position_end):
        """
        Args:
            staff (Staff):
            position_x (float):
            staff_position_start (int): Staff position where the stem starts
            staff_position_end (int): Staff position where the stem ends
        """
        super(Stem, self).__init__(staff, position_x)
        self._staff_position_start = staff_position_start
        self._staff_position_end = staff_position_end
        y_pos = self.staff._staff_pos_to_rel_pixels(self.staff_position_start)
        y_delta = (self.staff_position_start - self.staff_position_end) * self.staff.staff_unit
        self._grob = Path.straight_line(
            self.staff.x + self.position_x,
            self.staff.y + y_pos,
            0,
            y_delta,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def staff_position_start(self):
        """int: The starting staff position"""
        return self._staff_position_start

    @property
    def staff_position_end(self):
        """int: The ending staff position"""
        return self._staff_position_end

    @property
    def length_px(self):
        """int: The length in pixels of the ledger line"""
        return self._length_px

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
