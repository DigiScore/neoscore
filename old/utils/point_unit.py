#!/usr/bin/env python

from .base_unit import BaseUnit


class PointUnit(BaseUnit):
    """
    A unit in 72-dpi points
    """
    def __init__(self, value):
        """
        Args:
            value (int or float or PointUnit):
        """
        if isinstance(value, PointUnit):
            value = value.value
        elif not (isinstance(value, int) or isinstance(value, float)):
            try:
                value = float(value)
            except ValueError:
                raise TypeError('value in PointUnit.__init__() must be an int, float, or PointUnit')
        BaseUnit.__init__(self, value)

    def in_staff_units(self, reference):
        """
        Calculates and returns self.value in staff units relative to a given staff

        Args:
            reference (Staff or float or int): A reference staff or staff unit distance

        Returns: StaffUnit
        """
        from .staff_unit import StaffUnit
        from .staff import Staff
        # Maybe check type using type().__name__ instead to avoid importing Staff
        if isinstance(reference, Staff):
            return StaffUnit(self.value * reference.staff_unit_dist.value)
        elif isinstance(reference, float) or isinstance(reference, int):
            return StaffUnit(self.value * reference)
        else:
            raise TypeError('reference in PointUnit.in_staff_units() must be a Staff or number')

    def _allow_operators_with_numbers(self):
        return False

    def _return_number_when_using_operator_with_number(self):
        return False