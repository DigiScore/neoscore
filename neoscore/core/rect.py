from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Union

from typing_extensions import TypeAlias

from neoscore.core.point import Point
from neoscore.core.units import Unit


@dataclass(frozen=True)
class Rect:
    """A rectangle data class.

    The ``x`` and ``y`` coordinates represent the starting position,
    typically the top left corner. ``width`` and ``height`` extend
    rightward and downward.

    The only math operation supported for rects is scalar
    multiplication, where each field is multiplied by a given number.
    """

    x: Unit
    y: Unit
    width: Unit
    height: Unit

    @classmethod
    def from_def(cls, rect_def: RectDef) -> Rect:
        if isinstance(rect_def, Rect):
            return rect_def
        return cls(*rect_def)

    def offset(self, offset: Point) -> Rect:
        """Translate a rect by a point."""
        return Rect(self.x + offset.x, self.y + offset.y, self.width, self.height)

    def merge(self, other: Rect) -> Rect:
        """Find the rect encompassing both ``self`` and ``other``.

        Note: This assumes ``width`` and ``height`` in both rects are positive.
        """
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        right_edge = max(self.x + self.width, other.x + other.width)
        bottom_edge = max(self.y + self.height, other.y + other.height)
        return Rect(x, y, right_edge - x, bottom_edge - y)

    def __mul__(self, other: float) -> Rect:
        return Rect(
            self.x * other, self.y * other, self.width * other, self.height * other
        )


RectDef: TypeAlias = Union[Rect, Tuple[Unit, Unit, Unit, Unit]]
"""A ``Rect`` or an init arg tuple for one."""
