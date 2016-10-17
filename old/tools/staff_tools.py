#!/usr/bin/env python

from ..staff_unit import StaffUnit
from ..point_unit import PointUnit

# def y_of_staff_pos(staff, position, staff_space_offset=0):
#
#     """
#     Take a Staff and a position, and calculate the corresponding Y coordinate relative to the top of the staff
#
#     Args:
#         staff (Staff):
#         position (StaffUnit or float or int): position in staff units where 0 is the middle line
#         staff_space_offset (StaffUnit or float or int): Number of staff spaces to offset by.
#             For most cases this can be left at default 0.
#
#     Returns: PointUnit
#     """
#     if not isinstance(position, StaffUnit):
#         position = StaffUnit(position)
#     if not isinstance(staff_space_offset, StaffUnit):
#         staff_space_offset = StaffUnit(staff_space_offset)
#     # return (staff.staff_height.value / 2.0) + (-1 * staff.staff_unit_dist * (position + staff_space_offset))
#     staff_center = PointUnit(staff.staff_height.value / 2.0)
#     y_offset = StaffUnit((position.value + staff_space_offset.value) * -1).in_points(staff)
#     return staff_center + y_offset


def y_of_staff_pos(staff_attribute_set, position, staff_space_offset=0):

    """
    Take a StaffAttributeSet and a StaffUnit position, and calculate the corresponding
        Y coordinate relative to the top of the staff_attribute_set

    Args:
        staff_attribute_set (StaffAttributeSet):
        position (StaffUnit or float or int): position in staff_attribute_set units where 0 is the middle line
        staff_space_offset (StaffUnit or float or int): Number of staff_attribute_set spaces to offset by.
            For most cases this can be left at default 0.

    Returns: PointUnit
    """
    if not isinstance(position, StaffUnit):
        position = StaffUnit(position)
    if not isinstance(staff_space_offset, StaffUnit):
        staff_space_offset = StaffUnit(staff_space_offset)
    # return (staff.staff_height.value / 2.0) + (-1 * staff.staff_unit_dist * (position + staff_space_offset))
    staff_center = PointUnit(staff_attribute_set.height.value / 2.0)
    y_offset = StaffUnit((position.value + staff_space_offset.value) * -1).in_points(staff_attribute_set)
    return staff_center + y_offset


def line_or_space(staff_position):
    """

    Take a staff position and determine if it resides on a line or a space.

    Args:
        staff_position (StaffUnit):

    Returns: str ``'line'`` or ``'space'``

    """
    # Even numbered staff_position values belong on spaces
    if staff_position.value % 2 == 0:
        return 'line'
    else:
        return 'space'


# def needs_ledgers(staff, staff_position):
#     """
#     Whether or not the notehead will require ledger lines to draw
#
#     Args:
#         staff_position (StaffUnit):
#         staff (Staff):
#
#     Returns: bool
#     """
#     # Code taken & modified from Notehead.ledgers_needed
#     truncuated_staff_positition = abs(staff_position.value) - (staff.line_count - 1)
#     # If no ledgers are needed, return
#     if truncuated_staff_positition < 2:
#         return False
#     else:
#         return True

def needs_ledgers(staff_attribute_set, staff_position):
    """
    Whether or not the notehead will require ledger lines to draw

    Args:
        staff_attribute_set (StaffAttributeSet):
        staff_position (StaffUnit):

    Returns: bool
    """
    # This code is based on Notehead.ledgers_needed
    truncuated_staff_positition = abs(staff_position.value) - (staff_attribute_set.line_count - 1)
    # If no ledgers are needed, return
    if truncuated_staff_positition < 2:
        return False
    else:
        return True
