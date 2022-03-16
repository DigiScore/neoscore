from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

from neoscore.core.mapping import map_between
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.utils.point import Point
from neoscore.utils.units import Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Spanner2D(Spanner):
    def __init__(self, end_pos: Point, end_parent: Parent):
        super().__init__(end_pos.x, end_parent)
        self._end_y = end_pos.y

    @property
    def end_y(self) -> Unit:
        return self._end_y

    @end_y.setter
    def end_y(self, value: Unit):
        self._end_y = value

    @property
    def end_pos(self):
        # This could be stored, but it would make Spanner._end_x (set
        # in its constructor) redundant, so I prefer to keep end_pos
        # on-demand in both super and subclass for simplicity.
        return Point(self._end_x, self._end_y)

    @end_pos.setter
    def end_pos(self, value: Point):
        self._end_x = value.x
        self._end_y = value.y

    @property
    def spanner_2d_length(self) -> Unit:
        """The 2d length of the spanner.

        Note: This takes into account both the x and y axis. For only
            the horizontal length, use `spanner_x_length`.
        """
        if self.end_parent == self:
            relative_stop = self.end_pos
        else:
            relative_stop = (
                map_between(cast(PositionedObject, self), self.end_parent)
                + self.end_pos
            )
        distance = Unit(
            math.sqrt(
                (relative_stop.x.base_value**2) + (relative_stop.y.base_value**2)
            )
        )
        return type(cast(PositionedObject, self).pos.x)(distance)
