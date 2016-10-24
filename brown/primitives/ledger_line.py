from brown.core import brown
from brown.config import config
from brown.core.path import Path
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.utils import units



class LedgerLine(StaffObject):

    length = 1.75  # Staff units length of a ledger line

    def __init__(self, staff, position_x, staff_position):
        """
        Args:
            staff (Staff):
            position_x (float):
            staff_position (int): centered staff position
        """
        super(LedgerLine, self).__init__(staff, position_x)
        self._staff_position = staff_position
        self._length_px = LedgerLine.length * self.staff.staff_unit
        y_pos = self.staff._centered_position_to_rel_pixels(self.staff_position)
        print('ledger line staff y == {}'.format(self.staff.y))
        self._grob = Path.straight_line(
            self.staff.x + self.position_x - (self.length_px / 2),
            self.staff.y + y_pos,
            self.length_px,
            0,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def staff_position(self):
        """int: The centered staff position of the ledger line"""
        return self._staff_position

    @property
    def length_px(self):
        """int: The length in pixels of the ledger line"""
        return self._length_px

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()
