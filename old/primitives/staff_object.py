#!/usr/bin/env python

from .graphic_object import GraphicObject
from .tools.staff_tools import y_of_staff_pos
from .staff_unit import StaffUnit
from PySide import QtGui


class StaffObject(GraphicObject):
    """
    An abstract base class for objects which belong in a staff.

    Warnings:
        All handling of positions should be in StaffUnit units and go through StaffObject.x_staff_unit_pos and
        StaffObject.y_staff_unit_pos, access to the inherited x_pos and y_pos values should be considered protected
        by GraphicObject in the context of a StaffObject. Modifications made to StaffObject.x_staff_unit_pos and
        StaffObject.y_staff_unit_pos will automatically alter x_pos and y_pos
    """

    def __init__(self, parent_staff, x_staff_unit_pos, y_staff_unit_pos):
        """
        Args:
            parent_staff (Staff): The staff to which this StaffObject belongs
            x_staff_unit_pos (StaffUnit or int or float): The horizontal position of this StaffObject relative to the parent_staff
                Values below zero, though legal, will very rarely be useful
            y_staff_unit_pos (StaffUnit or int or float): y position in staff units where 0 is the center of the staff
        """
        self.parent_staff = parent_staff
        self.x_staff_unit_pos = x_staff_unit_pos
        self.y_staff_unit_pos = y_staff_unit_pos
        # y_pos = y_of_staff_pos(self.parent_staff, self.y_staff_pos)
        # GraphicObject.__init__(self, self.parent_staff, self.parent_staff.scene,
        #                        self.x_staff_unit_pos.in_points(self.parent_staff),
        #                        self.y_staff_unit_pos.in_points(self.parent_staff))
        GraphicObject.__init__(self, self.parent_staff, self.parent_staff.scene,
                               self.x_staff_unit_pos.in_points(self.staff_attributes),
                               y_of_staff_pos(self.staff_attributes, self.y_staff_unit_pos))
        # Register self in parent_staff.contents
        parent_staff.contents.append(self)

    @property
    def parent_staff(self):
        """
        Staff: a reference to the staff to which this StaffObject belongs
        """
        return self._parent_staff

    @parent_staff.setter
    def parent_staff(self, new_parent_staff):
        if not type(new_parent_staff).__name__ == 'Staff':
            raise TypeError('StaffObject.parent_staff must be of type Staff')
        self._parent_staff = new_parent_staff

    @property
    def staff_attributes(self):
        """StaffAttributeSet: The StaffAttributeSet currently active at self.x_staff_unit_pos"""
        return self.parent_staff.attributes_at(self.x_staff_unit_pos)

    @property
    def x_staff_unit_pos(self):
        """
        StaffUnit: The horizontal position of this StaffObject relative to the parent_staff.
                Values below zero, though legal, will very rarely be useful.
        """
        return self._x_staff_unit_pos
    
    @x_staff_unit_pos.setter
    def x_staff_unit_pos(self, new_value):
        if not isinstance(new_value, StaffUnit):
            new_value = StaffUnit(new_value)
        self._x_staff_unit_pos = new_value
        # Sync self._x_pos to the new value
        self._x_pos = self._x_staff_unit_pos.in_points(self.staff_attributes)
    
    @property
    def y_staff_unit_pos(self):
        """
        StaffUnit: The vertical position of this StaffObject relative to the parent_staff.
                A value of 0 means the object is places in the center of the staff.
                Lower values move down, higher values move up.
        """
        return self._y_staff_unit_pos
    
    @y_staff_unit_pos.setter
    def y_staff_unit_pos(self, new_value):
        if not isinstance(new_value, StaffUnit):
            new_value = StaffUnit(new_value)
        self._y_staff_unit_pos = new_value
        # Sync self._y_pos to the new value
        self._y_pos = y_of_staff_pos(self.staff_attributes, self._y_staff_unit_pos)

    # @property
    # def scene_space_x_pos(self):
    #     # Automatically calculate paper-space positions from the staff
    #     pass
    #
    # @property
    # def scene_space_y_pos(self):
    #     # Automatically calculate paper-space positions from the staff
    #     pass


    def build_glyph(self):
        raise NotImplementedError
