from enum import Enum


class PathElementType(Enum):
    """Enum for types of path elements"""
    move_to = 0
    line_to = 1
    curve_to = 2
    control_point = 3
