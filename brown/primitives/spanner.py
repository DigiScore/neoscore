import math

from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point


class Spanner:
    """A Mixin class for GraphicObjects with starting and ending anchors.

    This mixin only provides a common property interface for
    starting and ending anchors. It is up to the concrete object
    to determine how rendering logic should use this information.
    """

    def __init__(self, end_pos, end_parent=None):
        """
        Args:
            end_pos (Point or tuple init args): The position of the endpoint
            end_parent (GraphicObject or None): The parent of the endpoint.
                `end_pos` will be relative to this object.
                If None, this defaults to the spanner.
        """
        self.end_pos = (end_pos if isinstance(end_pos, Point)
                        else Point(*end_pos))
        self.end_parent = end_parent if end_parent else self

    ######## PUBLIC PROPERTIES ########

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
