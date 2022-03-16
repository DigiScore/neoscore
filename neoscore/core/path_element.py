from __future__ import annotations

from typing import TYPE_CHECKING

from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import Point

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class PathElement(PositionedObject):
    # TODO HIGH can this init be removed?
    def __init__(self, pos: Point, parent: Parent):
        super().__init__(pos, parent)


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
