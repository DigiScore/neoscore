#!/usr/bin/env python

from .tools.staff_tools import y_of_staff_pos
from .shared import brown_config
from .staff_object import StaffObject
from .point_unit import PointUnit
from .staff_unit import StaffUnit
from PySide.QtGui import QGraphicsLineItem, QPen, QBrush, QColor
from PySide.QtCore import Qt


class Stem(StaffObject):
    """
    A data container for stems.
    """
    def __init__(self, parent_column, y_staff_unit_anchor,
                 length='default', direction='default',
                 staff_position_end='default',
                 thickness='default'):
        """
        Args:
            parent_column (NoteColumn): The NoteColumn this stem belongs in
            y_staff_unit_anchor (StaffUnit or int or float): The starting staff
                position for the stem. For single noteheads this will be the
                notehead position. For chords this should either be the
                lowest or highest notehead position
            length (StaffUnit, int, float, or 'default'): The length of the
                stem in staff units. Leave as 'default' to use
                brown_config.default_stem_length, or if passing an explicit
                value to staff_position_end. If a value (other than 'default')
                is passed to staff_position_end, this value is ignored.
            direction (int or str): -1, 1, 'default', or 'flipped';
                the direction this stem faces. 1 points up, -1 points down.
                Use ``'default'`` or ``'flipped'`` to calculate direction
                based on ``y_staff_unit_anchor``
            staff_position_end (StaffUnit or int or float or 'default'):
                The ending point of the the Stem. If set to ``'default'`` the
                ending point will be automatically calculated. If a real
                value is passed both ``length`` and ``direction`` will
                be ignored.
        """
        StaffObject.__init__(self, parent_column.parent_staff,
                             parent_column.x_staff_unit_pos,
                             y_staff_unit_anchor)
        if length == 'default':
            self.length = brown_config.default_stem_length
        else:
            self.length = length
        if direction in ['default', 'flipped']:
            if self.y_staff_unit_pos < 0:
                self.direction = 1
            else:
                self.direction = -1
            if direction == 'flipped':
                self.direction *= -1
        else:
            self.direction = direction
        if thickness == 'default':
            self.thickness = brown_config.default_stem_thickness
        else:
            self.thickness = thickness

        if staff_position_end == 'default':
            # Calculate staff_position_end
            self.y_staff_unit_stop_pos = self.y_staff_unit_pos.value + (self.length.value * self.direction)
        else:
            # If a staff_position_end was specified, adjust self.length and
            # self.direction accordingly
            stem_distance = self.y_staff_unit_stop_pos - self.y_staff_unit_pos
            self.length = abs(stem_distance.value)
            if stem_distance.value < 0:
                self.direction = 1
            else:
                self.direction = -1

        # Shift self.x_staff_unit_pos based on the direction the stem faces
        if self.direction == 1:
            self.x_staff_unit_pos += self.staff_attributes.approx_notehead_width
        # Shift self.x_staff_unit_pos slightly right for alignment
        self.x_staff_unit_pos += StaffUnit(0.1)


    @property
    def direction(self):
        """int: The direction the staff faces. 1 if up, -1 if down."""
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if not (new_direction == -1 or new_direction == 1):
            raise ValueError('Stem.direction must be -1 or 1')
        self._direction = new_direction

    @property
    def length(self):
        """StaffUnit: The length of the stem. Setting this will automatically adjust self.y_stop_pos
        and self.staff_position_end accordingly"""
        return self._length

    @length.setter
    def length(self, new_length):
        if not isinstance(new_length, StaffUnit):
            new_length = StaffUnit(new_length)
        if new_length.value <= 0:
            raise ValueError('Stem.length must be greater than 0')
        if hasattr(self, '_length'):
            value_change = new_length - self._length
        else:
            value_change = StaffUnit(0)

        self._length = new_length
        # Adjust self.y_stop_pos and self.staff_position_end
        # self.staff_position_end = self.staff_position_start.value + (self._length.value * self.direction)
        # self.y_stop_pos = y_of_staff_pos(self.parent_staff, self.staff_position_end)
        # self.y_stop_pos = self.staff_position_end.in_points(self.parent_staff)
        # TODO: setting length no longer affects the y stopping position, this will cause modifications to length
        # TODO:     in NoteColumn._build_glyph in adjusting for column size to not correctly change the glyph
        if hasattr(self, '_y_staff_unit_stop'):
            self._y_staff_unit_stop += StaffUnit(value_change.value * self.direction)

    @property
    def thickness(self):
        """StaffUnit: """
        return self._thickness

    @thickness.setter
    def thickness(self, new_thickness):
        if not isinstance(new_thickness, StaffUnit):
            new_thickness = StaffUnit(new_thickness)
        self._thickness = new_thickness

    # @property
    # def staff_position_end(self):
    #     """StaffUnit: """
    #     return self._staff_position_end
    #
    # @staff_position_end.setter
    # def staff_position_end(self, new_staff_position_end):
    #     if not isinstance(new_staff_position_end, StaffUnit):
    #         new_staff_position_end = StaffUnit(new_staff_position_end)
    #     self._staff_position_end = new_staff_position_end

    @property
    def y_stop_pos(self):
        """PointUnit: """
        return self._y_stop

    @y_stop_pos.setter
    def y_stop_pos(self, new_y_stop):
        if not isinstance(new_y_stop, PointUnit):
            new_y_stop = PointUnit(new_y_stop)
        self._y_stop = new_y_stop

    @property
    def y_staff_unit_stop_pos(self):
        """StaffUnit: """
        return self._y_staff_unit_stop

    @y_staff_unit_stop_pos.setter
    def y_staff_unit_stop_pos(self, new_y_staff_unit_stop):
        if not isinstance(new_y_staff_unit_stop, StaffUnit):
            new_y_staff_unit_stop = StaffUnit(new_y_staff_unit_stop)
        self._y_staff_unit_stop = new_y_staff_unit_stop

    def build_glyph(self):
        self.glyph = StemGlyph(self)
        return self.glyph


class StemGlyph(QGraphicsLineItem):

    def __init__(self, stem):
        """
        Args:
            stem (Stem):
        """
        attribute_set = stem.staff_attributes
        y_start = y_of_staff_pos(attribute_set, stem.y_staff_unit_pos).value
        y_stop = y_of_staff_pos(attribute_set, stem.y_staff_unit_stop_pos).value
        QGraphicsLineItem.__init__(self, stem.x_pos.value, y_start, stem.x_pos.value, y_stop,
                                   stem.parent_staff.glyph, stem.scene)
        # self.setPen(QPen(QBrush(QColor(0, 0, 0)), thickness))
        line_pen = QPen(QBrush(QColor(*brown_config.default_color)), stem.thickness.in_points(attribute_set).value)
        line_pen.setCapStyle(Qt.PenCapStyle(Qt.RoundCap))
        self.setPen(line_pen)


