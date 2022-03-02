from dataclasses import dataclass

from brown.core.mapping import Positioned
from brown.utils.point import Point

# TODO HIGH Some real headaches coming up in ChordRest flags suggest
# these might need to be InvisibleObjects after all.. Otherwise some
# detailed work will be needed to ensure GraphicObjects really can
# have a bare `Positioned` like these as a parent and everything will
# work seamlessly.


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
