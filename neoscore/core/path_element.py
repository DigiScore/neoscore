from __future__ import annotations

from typing import TYPE_CHECKING

from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject

if TYPE_CHECKING:
    pass


class PathElement(PositionedObject):
    def __repr__(self) -> str:
        return f"{type(self).__name__}(pos={self.pos}, parent={self.parent})"


class MoveTo(PathElement):
    pass


class LineTo(PathElement):
    pass


class ControlPoint(PathElement):
    pass


class CurveTo(PathElement):
    def __init__(
        self,
        pos: Point,
        parent: PositionedObject,
        control_1: ControlPoint,
        control_2: ControlPoint,
    ):
        super().__init__(pos, parent)
        self.control_1 = control_1
        self.control_2 = control_2

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(pos={self.pos}, parent={self.parent},"
            + f" c1={self.control_1}, c2={self.control_2})"
        )
