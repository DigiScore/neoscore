#!/usr/bin/env python

import abc

from .point_unit import PointUnit


class LineBreak:
    """
    A representation of flowable break objects, such as line breaks, page breaks, and potentially others.
    """
    def __init__(self, parent_flowable_section, is_also_page_break=False, preserve_during_auto_breaks=False):
        """
        Args:
            parent_flowable_section (FlowableSection): The FlowableSection this LineBreak terminates
            is_also_page_break (bool): Whether or not this LineBreak is also a page break
            preserve_during_auto_breaks (bool): Whether or not this break should be
                preserved during auto-break generation.
        """
        self.parent_flowable_section = parent_flowable_section
        self.is_also_page_break = is_also_page_break
        self.preserve_during_auto_breaks = preserve_during_auto_breaks

    @property
    def parent_flowable(self):
        """Flowable: The flowable to which this break belongs"""
        return self.parent_flowable_section.parent_flowable

    @property
    def parent_flowable_section(self):
        """FlowableSection: The FlowableSection this break appears on"""
        return self._parent_flowable_section

    @parent_flowable_section.setter
    def parent_flowable_section(self, new_value):
        if not type(new_value).__name__ == 'FlowableSection':
            raise TypeError
        self._parent_flowable_section = new_value

    @property
    def x_flowable_space_pos(self):
        """PointUnit: The x position of this break relative to ``self.flowable``
            (in its virtual single-long-strip space)"""
        return self.parent_flowable_section.x_flowable_space_pos + self.parent_flowable_section.length

    @property
    def scene_pos_x(self):
        """PointUnit: The x position of where the line breaks (top right corner of the Flowable section)"""
        return self.parent_flowable_section.x_scene_space_pos + self.parent_flowable_section.length
    
    @property
    def scene_pos_y(self):
        """PointUnit: The y position of where the line breaks (top right corner of the parent FlowableSection)"""
        return self.parent_flowable_section.y_scene_space_pos
    
    @property
    def preserve_during_auto_breaks(self):
        """bool: This value is used during auto-break generation to determine if it can be deleted or not.
        User-defined breaks (preserve_during_auto_breaks == false) should be preserved during auto-break generation."""
        return self._preserve_during_auto_breaks

    @preserve_during_auto_breaks.setter
    def preserve_during_auto_breaks(self, new_value):
        self._preserve_during_auto_breaks = bool(new_value)

    @property
    def is_also_page_break(self):
        """bool: Whether or not this LineBreak is also a page break"""
        return self._is_also_page_break

    @is_also_page_break.setter
    def is_also_page_break(self, new_value):
        self._is_also_page_break = bool(new_value)
