from dataclasses import dataclass

from brown.core.types import Positioned
from brown.utils.point import Point


@dataclass(frozen=True)
class PathElement:

    pos: Point
    parent: Positioned

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


@dataclass(frozen=True)
class MoveTo(PathElement):
    pass


@dataclass(frozen=True)
class LineTo(PathElement):
    pass


@dataclass(frozen=True)
class ControlPoint:
    pos: Point
    parent: Positioned


@dataclass(frozen=True)
class CurveTo(PathElement):
    control_1: ControlPoint
    control_2: ControlPoint
