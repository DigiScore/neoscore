#!/usr/bin/env python

from .staff_unit import StaffUnit


class StaffUnitRectangle:
    """
    A primitive rectangle class in StaffUnit units with a number of convenience properties.
    """
    def __init__(self, x_pos, y_pos, width, height):
        """

        Args:
            x_pos (StaffUnit or float or int):
            y_pos (StaffUnit or float or int):
            width (StaffUnit or float or int):
            height (StaffUnit or float or int):

        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        if not isinstance(new_width, StaffUnit):
            new_width = StaffUnit(new_width)
        self._width = new_width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        if not isinstance(new_height, StaffUnit):
            new_height = StaffUnit(new_height)
        self._height = new_height

    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, new_x_pos):
        if not isinstance(new_x_pos, StaffUnit):
            new_x_pos = StaffUnit(new_x_pos)
        self._x_pos = new_x_pos

    @property
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, new_y_pos):
        if not isinstance(new_y_pos, StaffUnit):
            new_y_pos = StaffUnit(new_y_pos)
        self._y_pos = new_y_pos

    @property
    def left_edge(self):
        """StaffUnit: A convenience property giving the x coordinate of the left edge.
        Is equivalent to ``self.x_pos``"""
        return self.x_pos

    @property
    def right_edge(self):
        """StaffUnit: A convenience property giving the x coordinate of the right edge.
        Is equivalent to ``self.x_pos + self.width``"""
        return self.x_pos + self.width

    @property
    def top_edge(self):
        """StaffUnit: A convenience property giving the y coordinate of the top edge.
        Is equivalent to ``self.y_pos``"""
        return self.y_pos

    @property
    def bottom_edge(self):
        """StaffUnit: A convenience property giving the y coordinate of the bottom edge.
        Is equivalent to ``self.y_pos + self.height``"""
        return self.y_pos + self.height


