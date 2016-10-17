#!/usr/bin/env python

from .base_unit import BaseUnit


class StaffUnit(BaseUnit):
    """
    A unit representing the distance between an adjacent staff line and space.
    """
    def __init__(self, value):
        """
        Args:
            value (int or float or StaffUnit):
        """
        if isinstance(value, StaffUnit):
            value = value.value
        elif not (isinstance(value, int) or isinstance(value, float)):
            try:
                value = float(value)
            except ValueError:
                raise TypeError('value in StaffUnit.__init__() must be an int, float, or StaffUnit')

        # if not (isinstance(staff_unit_dist, int) or isinstance(staff_unit_dist, float)):
        #     raise TypeError('staff_unit_dist in StaffUnit.__init__() must be an int or float')
        # self.staff_unit_dist = staff_unit_dist
        BaseUnit.__init__(self, value)

    # def in_points(self, reference):
    #     """
    #     Converts self.value to 72-dpi points and returns it.
    #
    #     Args:
    #         reference (Staff, PointUnit, int, or float): The length of a staff unit
    #
    #     Returns: int or float
    #     """
    #     from .point_unit import PointUnit
    #     if type(reference).__name__ == 'PointUnit':
    #         reference = reference.value
    #     elif type(reference).__name__ == 'Staff':
    #         reference = reference.staff_unit_dist.value
    #     return PointUnit(self.value * reference)

    def in_points(self, reference):
        """
        Converts self.value to 72-dpi points and returns it.

        Args:
            reference (StaffAttributeSet or PointUnit or float or int): The length of a staff unit

        Returns: PointUnit
        """
        from .point_unit import PointUnit
        if type(reference).__name__ == 'PointUnit':
            reference = reference.value
        elif type(reference).__name__ == 'StaffAttributeSet':
            reference = reference.staff_unit_dist.value
        return PointUnit(self.value * reference)

    def _allow_operators_with_numbers(self):
        return False

    def _return_number_when_using_operator_with_number(self):
        return False
