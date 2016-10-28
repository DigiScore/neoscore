from brown.core.path import Path
from brown.primitives.staff_object import StaffObject


class Stem(StaffObject):

    def __init__(self, parent, position_x,
                 staff_position_start, staff_position_end):
        """
        Args:
            parent (StaffObject or Staff):
            position_x (float):
            staff_position_start (int): Staff position where the stem starts
            staff_position_end (int): Staff position where the stem ends
        """
        super().__init__(parent, position_x)
        self._staff_position_start = staff_position_start
        self._staff_position_end = staff_position_end
        y_pos = self.root_staff._staff_pos_to_rel_pixels(self.staff_position_start)
        y_delta = (self.staff_position_start - self.staff_position_end) * self.root_staff.staff_unit
        self._grob = Path.straight_line(
            self.position_x,
            y_pos,
            0,
            y_delta,
            self.parent.grob
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
