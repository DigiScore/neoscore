from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from neoscore.core.units import Unit


@dataclass(frozen=True)
class Rect:
    """A rectangle data class.

    The `x` and `y` coordinates represent the starting position,
    typically the top left corner. `width` and `height` extend
    rightward and downward.

    The only math operation supported for rects is scalar
    multiplication, where each field is multiplied by a given number.
    """

    x: Unit
    y: Unit
    width: Unit
    height: Unit

    def __mul__(self, other: float) -> Rect:
        return Rect(
            self.x * other, self.y * other, self.width * other, self.height * other
        )


RectDef = Union[Rect, tuple[Unit, Unit, Unit, Unit]]


def rect_from_def(rect_def: RectDef) -> Rect:
    if isinstance(rect_def, Rect):
        return rect_def
    return Rect(*rect_def)
