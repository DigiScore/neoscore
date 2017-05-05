from brown.core.graphic_object import GraphicObject
from brown.core.spanner import Spanner
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class HorizontalSpanner(Spanner):
    """A spanner which is perfectly horizontal.

    When in a Flowable, this spanner's end_y position always maps
    to the same y-axis position as its starting position in
    the Flowable's local space.

    Otherwise, this spanner's end_y position always maps to the same
    y-axis position as its starting position in document space.

    Like its Spanner superclass, this class is a mixin meant to be combined
    with GraphicObjects. Because the horizontal guarantees given by this
    spanner depend on the position of the GraphicObject starting position,
    it is crucial that, when initializing in implementation __init__ methods,
    this be initialized *after* the GraphicObject exists and has its intended
    `pos` and `parent` properties set.

    This differs from a typical spanner in that neither its end_y or end_pos
    attributes are settable. Only the end_x or end_parent properties may
    be modified.
    """

    def __init__(self, end_x, end_parent=None):
        """
        Args:
            end_x (Unit): The x-axis position of the endpoint
            end_parent (GraphicObject or None): The parent of the endpoint.
                `end_pos` will be relative to this object.
                If None, this defaults to the spanner.
        """
        self._end_x = end_x
        self.end_parent = end_parent if end_parent else self

    ######## PUBLIC PROPERTIES ########

    @property
    def end_x(self):
        """Unit: The x position of the endpoint"""
        return self._end_x

    @end_x.setter
    def end_x(self, value):
        self._end_pos.x = value

    @property
    def end_y(self):
        """Unit: The y position of the endpoint.

        Unlike that in `Spanner`, this property is read-only in order
        to maintain its horizontal guarantees.
        """
        if self.end_parent == self:
            return GraphicUnit(0)
        elif self.flowable is not None:
            return self.flowable.map_between_locally(
                self.end_parent, self).y
        else:
            return GraphicObject.map_between_items(self.end_parent, self).y

    @property
    def end_pos(self):
        """Point: The position of the endpoint"""
        return Point(self.end_x, self.end_y)
