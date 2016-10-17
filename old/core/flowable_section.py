#!/usr/bin/env python

from .line_break import LineBreak
from .point_unit import PointUnit


class FlowableSection:
    """
    A system representing a span of a flowable.
    """

    def __init__(self, parent_flowable, x_flowable_space_pos, length,
                 x_scene_space_pos, y_scene_space_pos):
        self.parent_flowable = parent_flowable
        self.x_flowable_space_pos = x_flowable_space_pos
        self.length = length
        self.x_scene_space_pos = x_scene_space_pos
        self.y_scene_space_pos = y_scene_space_pos
        # Build the terminating line break according to self.length
        self.terminating_line_break = LineBreak(self)

    @property
    def parent_flowable(self):
        """Flowable: The flowable to which this FlowableSection belongs"""
        return self._parent_flowable

    @parent_flowable.setter
    def parent_flowable(self, new_value):
        # FIXME: This is a terrible way to solve circular imports
        if not type(new_value).__name__ == 'Flowable':
            raise TypeError
        self._parent_flowable = new_value

    @property
    def x_flowable_space_pos(self):
        """PointUnit: Position in the virtual single-long-strip
        flowable where this system begins"""
        return self._x_flowable_space_pos

    @x_flowable_space_pos.setter
    def x_flowable_space_pos(self, new_value):
        self._x_flowable_space_pos = PointUnit(new_value)

    @property
    def x_scene_space_pos(self):
        """PointUnit: Position in scene space for the system"""
        return self._x_scene_space_pos

    @x_scene_space_pos.setter
    def x_scene_space_pos(self, new_value):
        self._x_scene_space_pos = PointUnit(new_value)

    @property
    def y_scene_space_pos(self):
        """PointUnit: Position in scene space for the system"""
        return self._y_scene_space_pos

    @y_scene_space_pos.setter
    def y_scene_space_pos(self, new_value):
        self._y_scene_space_pos = PointUnit(new_value)

    @property
    def length(self):
        """PointUnit: Length of this system in scene space"""
        return self._length

    @length.setter
    def length(self, new_value):
        self._length = PointUnit(new_value)
        # TODO: Adjusting length should trigger an adjustment of the position of the terminating line break (maybe?)

    @property
    def height(self):
        """PointUnit: Height of this system in scene space"""
        return self.parent_flowable.height

    @property
    def terminating_line_break(self):
        """LineBreak: The Linebreak marking the system end"""
        return self._terminating_line_break

    @terminating_line_break.setter
    def terminating_line_break(self, new_value):
        if not isinstance(new_value, LineBreak):
            raise TypeError
        self._terminating_line_break = new_value
        # TODO: Adjusting the terminating line break should trigger an adjustment of length (maybe?)
