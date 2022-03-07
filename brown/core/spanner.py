import math
from typing import Optional, cast

from brown.core.graphic_object import GraphicObject
from brown.core.mapping import Positioned, map_between, map_between_x
from brown.utils.point import Point
from brown.utils.units import Unit


class Spanner:
    """A Mixin class for `GraphicObject`s with starting and ending anchors.

    If the spanner (main `GraphicObject`) is in a `Flowable`, the endpoint
    must be in the same one. Likewise, if the spanner is *not* in one,
    the endpoint must not be in one either.

    This mixin only provides a common interface for ending anchors.
    The starting position of this spanner should be the main object's
    `GraphicObject.pos`, and the starting anchor should be the its
    `GraphicObject.parent`. It is up to the implementing class to
    decide how to use this information.
    """

    def __init__(self, end_pos: Point, end_parent: Optional[Positioned] = None):
        """
        Args:
            end_pos: The position of the endpoint
            end_parent: The parent of the endpoint. `end_pos` will be relative to
                this object. If None, this defaults to `self`.

        Warning: If the spanner is in a `Flowable`, `end_parent` must be
            in the same one. Likewise, if the spanner is not in a
            `Flowable`, this must not be either.
        """
        self._end_pos = end_pos
        self._end_parent = end_parent if end_parent else cast(Positioned, self)

    ######## PUBLIC PROPERTIES ########

    @property
    def end_x(self) -> Unit:
        """The x position of the endpoint"""
        return self._end_pos.x

    @end_x.setter
    def end_x(self, value: Unit):
        self._end_pos = Point(value, self._end_pos.y)

    @property
    def end_y(self) -> Unit:
        """The y position of the endpoint"""
        return self._end_pos.y

    @end_y.setter
    def end_y(self, value: Unit):
        self._end_pos = Point(self._end_pos.x, value)

    @property
    def end_pos(self) -> Point:
        """The position of the endpoint"""
        return self._end_pos

    @end_pos.setter
    def end_pos(self, value: Point):
        self._end_pos = value

    @property
    def end_parent(self) -> Positioned:
        """The parent of the endpoint. This may be `self`."""
        return self._end_parent

    @end_parent.setter
    def end_parent(self, value: Positioned):
        self._end_parent = value

    @property
    def spanner_x_length(self) -> Unit:
        """The x-axis length of the spanner.

        Implementing subclasses will often want to override
        `GraphicObject.length` to return this.
        """
        if self.end_parent == self:
            return self.end_pos.x
        else:
            return (
                map_between_x(cast(Positioned, self), self.end_parent) + self.end_pos.x
            )

    @property
    def spanner_length(self) -> Unit:
        """The 2d length of the spanner.

        Note: This takes into account both the x and y axis. For only
            the horizontal length, use `spanner_x_length`.
        """
        if self.end_parent == self:
            relative_stop = self.end_pos
        else:
            relative_stop = (
                map_between(cast(Positioned, self), self.end_parent) + self.end_pos
            )
        distance = Unit(
            math.sqrt(
                (relative_stop.x.base_value**2) + (relative_stop.y.base_value**2)
            )
        )
        return type(cast(Positioned, self).pos.x)(distance)
