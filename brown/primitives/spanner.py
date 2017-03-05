import math

from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point


class Spanner:
    """A Mixin class for GraphicObjects with starting and ending anchors.

    If the spanner (main GraphicObject) is in a FlowableFrame, the endpoint
    must be in the same one. Likewise, if the spanner is *not* in one,
    the endpoint must not be in one either.

    This mixin only provides a common property interface for
    starting and ending anchors. It is up to the concrete object
    to determine how rendering logic should use this information.

    This class is a mixin meant to be combined with GraphicObjects.
    In the implementing class's `__init__` method, the Spanner class
    should be initialized after the GraphicObject.
    """

    def __init__(self, end_pos, end_parent=None):
        """
        Args:
            end_pos (Point or tuple init args): The position of the endpoint
            end_parent (GraphicObject or None): The parent of the endpoint.
                `end_pos` will be relative to this object.
                If None, this defaults to the spanner.

        Warning: If the spanner is in a FlowableFrame, `end_parent` must be
            in the same one. Likewise, if the spanner is not in a
            FlowableFrame, this must not be either.
        """
        self._end_pos = (end_pos if isinstance(end_pos, Point)
                         else Point(*end_pos))
        self.end_parent = end_parent if end_parent else self

    ######## PUBLIC PROPERTIES ########

    @property
    def end_x(self):
        """Unit: The x position of the endpoint"""
        return self._end_pos.x

    @end_x.setter
    def end_x(self, value):
        self._end_pos.x = value

    @property
    def end_y(self):
        """Unit: The y position of the endpoint"""
        return self._end_pos.y

    @end_y.setter
    def end_y(self, value):
        self._end_pos.y = value

    @property
    def end_pos(self):
        """Point: The position of the endpoint"""
        return self._end_pos

    @end_pos.setter
    def end_pos(self, value):
        self._end_pos = value

    @property
    def length(self):
        """Unit: The length of the spanner.

        The exact unit type will be the type of `self.start.x`
        """
        if self.end_parent == self:
            relative_stop = Point.from_existing(self.end_pos)
        else:
            relative_stop = (
                GraphicObject.map_between_items(
                    self,
                    self.end_parent)
                + self.end_pos)
        relative_stop.to_unit(type(self.pos.x))
        distance = math.sqrt((relative_stop.x.value ** 2)
                             + (relative_stop.y.value ** 2))
        return type(self.pos.x)(distance)
