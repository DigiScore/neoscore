#!/usr/bin/env python


def mm_to_pt(mm_value):
    """
    Converts a given value in millimeters to 72-DPI Points.

    Args:
        mm_value (float):

    Returns: float
    """
    return mm_value * 2.8346472


def pt_to_mm(pt_value):
    """
    Converts a given value in 72-DPI Points to millimeters

    Args:
        pt_value (float):

    Returns: float

    """
    return pt_value / 2.8346472


def staff_unit_to_pt(staff_unit_dist, staff_unit_value):
    """
    Converts a given value in staff units to 72-dpi points

    Args:
        staff_unit_dist (float): The unit distance of the reference staff in 72-dpi points
        staff_unit_value (float): Where 1 staff unit is the distance between a
            staff line and the center of an adjacent staff space

    Returns: float

    """
    return staff_unit_dist * staff_unit_value
