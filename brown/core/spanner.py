from typing import Optional, Union, cast

from brown.core.graphic_object import GraphicObject
from brown.core.mapping import Positioned, map_between, map_between_x
from brown.utils.point import Point
from brown.utils.units import ZERO, Unit


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

    Simple `Spanner`s are horizontal relative to their starting
    anchor. Arbitrary end-y positions can be set with `Spanner2D`.
    """

    def __init__(self, end_x: Unit, end_parent: Positioned):
        """
        Args:
            end_pos: The position of the endpoint. If a `Unit` is given, it will be
                treated as the end X position, and the end Y position will be
                calculated to be horizontal relative to the start.
            end_parent: The parent of the endpoint. `end_pos` will be relative to
                this object. If None, this defaults to `self`.

        Warning: If the spanner is in a `Flowable`, `end_parent` must be
            in the same one. Likewise, if the spanner is not in a
            `Flowable`, this must not be either.
        """
        self._end_x = end_x
        self._end_parent = end_parent

    @property
    def end_x(self) -> Unit:
        """The x position of the endpoint"""
        return self._end_x

    @end_x.setter
    def end_x(self, value: Unit):
        self._end_x = value

    @property
    def end_y(self) -> Unit:
        """The y position of the endpoint"""
        return map_between(self.end_parent, cast(Positioned, self)).y

    @property
    def end_pos(self) -> Point:
        """The position of the endpoint"""
        return Point(self.end_x, self.end_y)

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
