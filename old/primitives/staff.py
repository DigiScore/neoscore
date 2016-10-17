#!/usr/bin/env python
from PySide.QtGui import QGraphicsItem
from PySide.QtCore import QRectF
from .graphic_object import GraphicObject
from .clef import Clef
from .shared import brown_config
from .staff_unit import StaffUnit
from .point_unit import PointUnit
from PySide.QtGui import QPen, QBrush, QColor
import collections


class Staff(GraphicObject):
    def __init__(self, parent, scene, x_pos, y_pos, length, staff_unit_dist,
                 line_count=5, line_width='default',
                 is_visible=True):
        # TODO: Move many properties upstream to a parent_system (System) object
        """

        Args:
            parent (QGraphicsItem or None):
            scene (QGraphicsScene):
            x_pos (PointUnit or int or float):
            y_pos (PointUnit or int or float):
            length (StaffUnit or int or float): Length of the staff
            staff_unit_dist (PointUnit or int or float):
            line_count (int):
            line_width (StaffUnit or float or int or 'default'):
            is_visible (bool): Whether or not the staff will be drawn

        """
        GraphicObject.__init__(self, parent, scene, x_pos, y_pos)
        self._contents = []
        # Convert line_width to a value if needed
        if line_width == 'default':
            line_width = brown_config.default_staff_line_width
        # Pass arguments to an initial StaffAttributeSet placed at the
        # beginning of the staff
        self._staff_attribute_set_list = StaffAttributeSetList(self)
        self._staff_attribute_set_list.add_attribute_set(0, length, is_visible,
                                                         staff_unit_dist,
                                                         line_count,
                                                         line_width)
        self.build_glyph()

    def clef_at_position(self, x_staff_unit_pos):
        """
        Calculates the current clef at a given horizontal x_staff_unit_start

        Args:
            x_staff_unit_pos (StaffUnit or float or int):

        Returns: Clef object
        """
        clef = min([item for item in self.contents if
                    (isinstance(item, Clef) and item.x_staff_unit_pos < x_staff_unit_pos)],
                   key=lambda item: x_staff_unit_pos - item.x_staff_unit_pos)
        if clef is None:
            raise NoClefError
        return clef

    @property
    def contents(self):
        """list: A list of the contents of this Staff"""
        return self._contents

    @property
    def staff_attribute_set_list(self):
        """StaffAttributeSetList: """
        return self._staff_attribute_set_list

    @property
    def total_length(self):
        """PointUnit: The total length of this Staff"""
        # Find the total length by looking through every StaffAttributeSet and
        # adding their lengths in PointUnit units
        length = PointUnit(0)
        for point in self.staff_attribute_set_list:
            length += point.length.in_points(point.staff_unit_dist)
        return length

    @property
    def total_height(self):
        """PointUnit: The total height of this Staff"""
        # Find the total height by looking through every StaffAttributeSet and
        # finding the one with the greatest height
        return max([point.height for point in self.staff_attribute_set_list],
                   key=lambda height: height.value)

    def attributes_at(self, x_staff_unit_pos):
        """
        Find the active StaffAttributeSet at a given x_staff_unit_start

        Wraps ``self.staff_attribute_set_list.attributes_at(x_staff_unit_pos)``

        Args:
            x_staff_unit_pos (StaffUnit or float or int):

        Returns: StaffAttributeSet
        """
        return self.staff_attribute_set_list.attributes_at(x_staff_unit_pos)

    def add_attribute_set(self, effect_start_pos, length, visible, staff_unit_dist, line_count, line_width):
        """
        Add a StaffAttributeSet to self.staff_attribute_set_list

        Wraps ``self.staff_attribute_set_list.append(StaffAttributeSet())`` where
        StaffAttributeSet.parent_attribute_set_list is automatically assigned to this object's StaffAttributeSetList

        Args:
            effect_start_pos (StaffUnit or float or int): The x position from which this StaffAttributeSet
                begins taking effect. This set of attributes will be in effect unless another StaffAttributeSet is
                encountered in the parent staff.
            length (StaffUnit or float or int): the length of the section of staff this StaffAttributeSet
                is in effect
            visible (bool or 'revert' or 'keep'):
            staff_unit_dist (PointUnit or float or int or 'revert' or 'keep'):
            line_count (int or 'revert' or 'keep'):
            line_width (StaffUnit or float or int or 'revert' or 'keep'):

        Returns: None

        Notes: Passing ``'revert'`` to arguments will take the value of the ``StaffAttributeSet`` active before the one
        active at ``effect_start_pos``, ``'keep'`` will keep the value of the currently active ``StaffAttributeSet` at
        ``effect_start_pos`
        """
        self.staff_attribute_set_list.add_attribute_set(effect_start_pos, length, visible,
                                                        staff_unit_dist, line_count, line_width)

    def add_attribute_revert_to_previous(self, effect_start_pos, length):
        """
        Add a StaffAttributeSet to self.staff_attribute_set_list at a given point which switches to the
            StaffAttributeSet before the one active at effect_start_pos

        Args:
            effect_start_pos (StaffUnit or float or int):
            length (StaffUnit or float or int):

        Returns: None

        Notes: If effect_start_pos is placed at a point in the staff where there is no previous StaffAttributeSet
            to revert to, this will have no effect.
        """
        # Find the previously active StaffAttributeSet
        self.add_attribute_set(effect_start_pos, length, 'revert', 'revert', 'revert', 'revert')

    def add_cutout_region(self, effect_start_pos, length):
        """
        Cut out a region of the drawn staff, preserving overall length and attributes

        Args:
            effect_start_pos (StaffUnit or float or int): Cut-out starting position
            length (StaffUnit or float or int): Length of the cut-out region

        Returns: None

        Notes: This probably won't work if the cut-out region overlaps with more than one staff attribute region
        """
        if not isinstance(effect_start_pos, StaffUnit):
            effect_start_pos = StaffUnit(effect_start_pos)
        if not isinstance(length, StaffUnit):
            length = StaffUnit(length)
        span_length = self.attributes_at(effect_start_pos).length
        tail_pos = effect_start_pos + length
        tail_length = span_length - length
        self.add_attribute_set(effect_start_pos, length, False, 'keep', 'keep', 'keep')
        if tail_length.value > 0:
            self.add_attribute_revert_to_previous(tail_pos, tail_length)

    def build_glyph(self):
        # if self.glyph:
        #     self.scene.removeItem(self.glyph)
        self.glyph = StaffGlyph(self)
        return self.glyph


class StaffAttributeSetList(collections.MutableSequence):
    """
    A manager of a list of StaffAttributeSet objects.

    Adding items to this list may be called by the convenience method ``add_attribute_set_list``,
        or by using an explicit `.append(StaffAttributeSet(...))``
    """
    def __init__(self, parent_staff):
        self.parent_staff = parent_staff
        self.list = []

    @property
    def parent_staff(self):
        """Staff: The staff to which this object belongs"""
        return self._parent_staff

    @parent_staff.setter
    def parent_staff(self, new_parent_staff):
        if not isinstance(new_parent_staff, Staff):
            raise TypeError
        self._parent_staff = new_parent_staff

    def _refresh_list(self):
        """
        Refresh self.attribute_set_list, ordering according to x_staff_unit_pos values and modifying lengths to correct
            overlapping StaffAttributeSet regions

        Returns: None
        """
        # If there is 1 or fewer (0) objects in self.attribute_set_list, there is nothing to do here. Return.
        if len(self.list) <= 0:
            return
        # Re-order according to x_staff_unit_pos values (lowest first)
        self.list = sorted(self.list, key=lambda item: item.effect_start_pos.value)
        # Adjust lengths so that all StaffAttributeSet items are continuous
        # (Start from index 1 to skip the first attribute set)
        for i in range(1, len(self.list)):
            previous_set = self.list[i - 1]
            current_set = self.list[i]
            # if previous_set.x_staff_unit_start + previous_set.length != current_set.x_staff_unit_start:
            previous_set.length = current_set.effect_start_pos - previous_set.effect_start_pos

    def add_attribute_set(self, effect_start_pos, length, visible, staff_unit_dist, line_count, line_width):
        """
        A convenience method wrapping ``self.append(StaffAttributeSet())`` where
        StaffAttributeSet.parent_attribute_set_list is automatically assigned to this StaffAttributeSetList

        Args:
            effect_start_pos (StaffUnit or float or int): The x position from which this StaffAttributeSet
                begins taking effect. This set of attributes will be in effect unless another StaffAttributeSet is
                encountered in the parent staff.
            length (StaffUnit or float or int): the length of the section of staff this StaffAttributeSet
                is in effect
            visible (bool or 'revert' or 'keep'):
            staff_unit_dist (PointUnit or float or int or 'revert' or 'keep'):
            line_count (int or 'revert' or 'keep'):
            line_width (StaffUnit or float or int or 'revert' or 'keep'):

        Returns: None

        Notes: Passing ``'revert'`` to arguments will take the value of the ``StaffAttributeSet`` active before the one
        active at ``effect_start_pos``, ``'keep'`` will keep the value of the currently active ``StaffAttributeSet` at
        ``effect_start_pos`
        """
        self.append(StaffAttributeSet(self, effect_start_pos, length, visible, staff_unit_dist, line_count, line_width))

    def attributes_at(self, x_staff_unit_pos):
        """
        Find the active StaffAttributeSet at a given x_staff_unit_start

        Args:
            x_staff_unit_pos (StaffUnit or float or int):

        Returns: StaffAttributeSet
        """
        staff_attribute_set = min([point for point in self if
                                   point.effect_start_pos <= x_staff_unit_pos],
                                  key=lambda point: abs(x_staff_unit_pos.value - point.effect_start_pos.value))
        if staff_attribute_set is not None:
            return staff_attribute_set
        else:
            raise NoStaffAttributeSetError

    def previously_active_attribute_set_at(self, x_staff_unit_pos):
        """
        Find the StaffAttributeSet active before the currently active one at a given x staff unit position.
        Return None if there is no previously active StaffAttributeSet at the given x staff unit position

        Args:
            x_staff_unit_pos (StaffUnit or float or int):

        Returns: StaffAttributeSet or None
        """
        previous_index = self.index(self.attributes_at(x_staff_unit_pos)) - 1
        if previous_index >= 0:
            return self[previous_index]
        else:
            return None

    def _check_type(self, item):
        if not isinstance(item, StaffAttributeSet):
            raise ValueError

    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __delitem__(self, index):
        del self.list[index]
        self._refresh_list()

    def __setitem__(self, index, value):
        self._check_type(value)
        self.list[index] = value
        self._refresh_list()

    def insert(self, index, value):
        self._check_type(value)
        self.list.insert(index, value)
        self._refresh_list()


class StaffAttributeSet:

    """
    A collection of staff attributes to be contained in a StaffAttributePoint
    """

    def __init__(self, parent_attribute_set_list, effect_start_pos, length, visible,
                 staff_unit_dist, line_count, line_width):
        """

        Args:
            parent_attribute_set_list (StaffAttributeSetList): The StaffAttributeSetList to which this belongs
            effect_start_pos (StaffUnit or float or int): The x position from which this StaffAttributeSet
                begins taking effect. This set of attributes will be in effect unless another StaffAttributeSet is
                encountered in the parent staff.
            length (StaffUnit or float or int): the length of the section of staff this StaffAttributeSet
                is in effect
            visible (bool or 'revert' or 'keep'):
            staff_unit_dist (PointUnit or float or int or 'revert' or 'keep'):
            line_count (int or 'revert' or 'keep'):
            line_width (StaffUnit or float or int or 'revert' or 'keep'):

        Notes:  Passing ``'revert'`` to arguments will take the value of the ``StaffAttributeSet`` active before the one
        active at ``effect_start_pos``, ``'keep'`` will keep the value of the currently active ``StaffAttributeSet` at
        ``effect_start_pos`

        """
        self.parent_attribute_set_list = parent_attribute_set_list
        self.effect_start_pos = effect_start_pos
        self.length = length
        self.staff_unit_dist = staff_unit_dist
        self.is_visible = visible
        self.line_count = line_count
        self.line_width = line_width

    @property
    def parent_attribute_set_list(self):
        """Staff: The staff to which this StaffAttributeSet belongs"""
        return self._parent_attribute_set_list

    @parent_attribute_set_list.setter
    def parent_attribute_set_list(self, new_set_list):
        if not isinstance(new_set_list, StaffAttributeSetList):
            raise TypeError
        self._parent_attribute_set_list = new_set_list

    @property
    def line_count(self):
        """int: The number of lines in the staff"""
        return self._line_count

    @line_count.setter
    def line_count(self, new_value):
        if new_value == 'revert':
            new_value = self.parent_attribute_set_list.previously_active_attribute_set_at(
                    self.effect_start_pos).line_count
        elif new_value == 'keep':
            new_value = self.parent_attribute_set_list.attributes_at(self.effect_start_pos).line_count
        if not isinstance(new_value, int):
            raise TypeError('StaffAttributeSet.line_count must be an int')
        if new_value < 1:
            raise ValueError('StaffAttributeSet.line_count must be an int greater than 0')
        self._line_count = new_value

    @property
    def line_width(self):
        """StaffUnit: The width of staff lines.
        Ledger lines belonging in this Staff will take on this value."""
        return self._line_width

    @line_width.setter
    def line_width(self, new_value):
        if new_value == 'revert':
            new_value = self.parent_attribute_set_list.previously_active_attribute_set_at(
                    self.effect_start_pos).line_width
        elif new_value == 'keep':
            new_value = self.parent_attribute_set_list.attributes_at(self.effect_start_pos).line_width
        if not isinstance(new_value, StaffUnit):
            new_value = StaffUnit(new_value)
        self._line_width = new_value

    @property
    def is_visible(self):
        """
        bool: Whether or not the staff will be drawn
        """
        return self._is_visible

    @is_visible.setter
    def is_visible(self, new_value):
        if new_value == 'revert':
            new_value = self.parent_attribute_set_list.previously_active_attribute_set_at(
                            self.effect_start_pos).is_visible
        elif new_value == 'keep':
            new_value = self.parent_attribute_set_list.attributes_at(self.effect_start_pos).is_visible
        if not isinstance(new_value, bool):
            raise TypeError('StaffAttributeSet.is_visible must be of type bool')
        self._is_visible = new_value

    @property
    def staff_unit_dist(self):
        """PointUnit: The distance in 72-dpi points that a StaffUnit occupies within this Staff"""
        return self._staff_unit_dist

    @staff_unit_dist.setter
    def staff_unit_dist(self, new_value):
        if new_value == 'revert':
            new_value = self.parent_attribute_set_list.previously_active_attribute_set_at(
                    self.effect_start_pos).staff_unit_dist
        elif new_value == 'keep':
            new_value = self.parent_attribute_set_list.attributes_at(self.effect_start_pos).staff_unit_dist
        if not isinstance(new_value, PointUnit):
            new_value = PointUnit(new_value)
        self._staff_unit_dist = new_value

    @property
    def effect_start_pos(self):
        """
        StaffUnit: The horizontal position of this StaffAttributePoint relative to the parent_staff.
                Values below zero, though legal, will very rarely be useful.
        """
        return self._effect_start_pos

    @effect_start_pos.setter
    def effect_start_pos(self, new_value):
        if not isinstance(new_value, StaffUnit):
            new_value = StaffUnit(new_value)
        self._effect_start_pos = new_value

    @property
    def length(self):
        """StaffUnit: The length for which this StaffAttributePoint is in effect"""
        return self._length

    @length.setter
    def length(self, new_length):
        if not isinstance(new_length, StaffUnit):
            new_length = StaffUnit(new_length)
        self._length = new_length

    @property
    def height(self):
        """PointUnit: The height of the staff area for which this StaffAttributePoint is in effect"""
        return StaffUnit((self.line_count * 2) - 1).in_points(self.staff_unit_dist)

    @property
    def approx_notehead_width(self):
        """PointUnit: the typical width of a notehead placed within this staff"""
        return StaffUnit(2.25)

    @property
    def x_point_unit_start(self):
        """PointUnit: The point where this StaffAttributeSet begins taking effect"""
        # Find the position by going through all StaffAttributeSet objects in the parent staff to the left
        # and adding their lengths in PointUnit units
        x_point_unit_pos = PointUnit(0)
        for attribute_set in self.parent_attribute_set_list:
            if attribute_set.effect_start_pos < self.effect_start_pos:
                x_point_unit_pos += attribute_set.length.in_points(attribute_set)
        return x_point_unit_pos


class StaffGlyph(QGraphicsItem):
    def __init__(self, staff):
        """
        Args:
            staff (Staff):
        """
        QGraphicsItem.__init__(self, parent=staff.parent, scene=staff.scene)
        self.setPos(staff.x_pos.value, staff.y_pos.value)
        self.staff = staff

    def paint(self, painter, option, widget):
        for staff_attribute_set in self.staff.staff_attribute_set_list:
            # Don't draw staff regions that are marked invisible
            if not staff_attribute_set.is_visible:
                continue
            # Find the distance between staff lines
            # Find x start and stop
            line_step = staff_attribute_set.staff_unit_dist.value * 2
            x_start = staff_attribute_set.x_point_unit_start
            x_stop = x_start + staff_attribute_set.length.in_points(staff_attribute_set)
            for i in range(staff_attribute_set.line_count):
                line_width = staff_attribute_set.line_width.in_points(staff_attribute_set)
                current_y = line_step * i
                painter.setPen(QPen(QBrush(QColor(*brown_config.default_color)), line_width.value))
                painter.drawLine(x_start.value, current_y, x_stop.value, current_y)

    def boundingRect(self):
        return QRectF(0, 0, self.staff.total_length.value, self.staff.total_height.value)


class NoClefError(Exception):
    """
    Appears when a staff has no active clef at a given tested point
    """
    pass


class NoStaffAttributeSetError(Exception):
    """
    Appears when a staff has no active StaffAttributePoint at a given tested point
    """
    pass
