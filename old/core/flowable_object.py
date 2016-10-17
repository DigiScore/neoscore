#!/usr/bin/env python

from .graphic_object import GraphicObject
from .flowable import Flowable


class FlowableObject(GraphicObject):
    """
    An abstract GraphicObject which is contained inside a Flowable and uses
    special methods for glyph building that allow wrapping across flowable
    sections
    """

    def __init__(self, parent, scene, parent_flowable, x_pos, y_pos):
        """
        Args:
            parent (QGraphicsItem):
            scene (QGraphicsScene):
            parent_flowable (Flowable):
            x_pos (PointUnit): Coordinate in flowable space
            y_pos (PointUnit): Coordinate in flowable space
        """
        GraphicObject.__init__(self, parent, scene, x_pos, y_pos)
        self.parent_flowable = parent_flowable

    @property
    def parent_flowable(self):
        """Flowable: The Flowble which contains this GraphicObject"""
        return self._parent_flowable

    @parent_flowable.setter
    def parent_flowable(self, new_value):
        if not isinstance(new_value, Flowable):
            raise TypeError
        self._parent_flowable = new_value

    def build_glyph(self):
        raise NotImplementedError

    # def build_glyph_complete(self):
    #     raise NotImplementedError
    #
    # def build_glyph_start(self):
    #     raise NotImplementedError
    #
    # def build_glyph_continue(self):
    #     raise NotImplementedError
    #
    # def build_glyph_end(self):
    #     raise NotImplementedError