from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from brown.utils.point import Point
from brown.utils.units import Unit


@dataclass(frozen=True)
class Rect:
    """A rectangle data class.

    The `x` and `y` coordinates represent the starting position,
    typically the top left corner. `width` and `height` extend
    rightward and downward.
    """

    # TODO Rect should probably be Unit-only, so it aligns with Point
    # semantics and doesn't cause type collisions in places where Rect
    # uses Unit. I think the float variant is only used in a few
    # low-level Qt contexts, where it could probably be replaced with
    # QRectF anyway.

    x: Union[Unit, float]
    y: Union[Unit, float]
    width: Union[Unit, float]
    height: Union[Unit, float]

    def in_unit(self, unit: Unit) -> Rect:
        """Derive a new rectangle from this one in a given unit.

        If properties are already units, they are converted to
        equivalent given units. If properties are numbers, they are
        used as inputs in the given unit.
        """
        return Rect(unit(self.x), unit(self.y), unit(self.width), unit(self.height))

    @property
    def pos(self):
        """Point: The starting (usually top-left) corner of the rect"""
        return Point(self.x, self.y)
