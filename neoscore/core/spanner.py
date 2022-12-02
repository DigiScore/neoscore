from __future__ import annotations

from typing import cast

from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.units import Unit


class Spanner:
    """Mixin for a :obj:`.PositionedObject` with starting and ending anchors.

    If the spanner is in a :obj:`.Flowable`, the endpoint must be in the same one.
    Likewise, if the spanner is *not* in one, the endpoint must not be in one either.

    This mixin only provides a common interface for ending anchors. The starting
    position of this spanner should be the main object's ``PositionedObject.pos``, and
    the starting anchor should be its ``PositionedObject.parent``. It is up to the
    implementing class to decide how to use this information.

    Simple ``Spanner``\ s are horizontal relative to their starting anchor. Arbitrary
    end-y positions can be set with :obj:`.Spanner2D`.
    """

    def __init__(self, end_x: Unit, end_parent: PositionedObject):
        """
        Args:
            end_x: The X position of the endpoint.
            end_parent: The parent of the endpoint. ``end_x`` will be relative to
                this object. This can be the spanner itself to make it relative to
                the starting point.
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

    @render_cached_property
    def end_y(self) -> Unit:
        """The y position of the endpoint.

        This value is automatically computed such that the spanner is horizontal.
        """
        return self.end_parent.map_to(cast(PositionedObject, self)).y

    @property
    def end_pos(self) -> Point:
        """The position of the endpoint"""
        return Point(self.end_x, self.end_y)

    @property
    def end_parent(self) -> PositionedObject:
        """The parent of the endpoint. This may be ``self``."""
        return self._end_parent

    @end_parent.setter
    def end_parent(self, value: PositionedObject):
        self._end_parent = value

    @render_cached_property
    def spanner_x_length(self) -> Unit:
        """The x-axis length of the spanner."""
        if self.end_parent == self:
            return self.end_pos.x
        else:
            return (
                cast(PositionedObject, self).map_x_to(self.end_parent) + self.end_pos.x
            )

    @property
    def breakable_length(self) -> Unit:
        """Spanners are breakable over their ``spanner_x_length``."""
        return self.spanner_x_length

    def point_along_spanner(self, ratio: float) -> Point:
        """Find the point on the spanner at a given 0-1 ratio along it.

        For example, a ratio of ``0.5`` will give the point half-way along the spanner.

        The returned point will be relative to the starting point.

        Args:
            ratio: A value representing progress along the spanner,
                where 0 is at the start and 1 is at the end. Values outside these
                bounds will give a point as if the spanner extended to infinity.
        """
        return (
            cast(PositionedObject, self).map_to(self.end_parent) + self.end_pos
        ) * ratio
