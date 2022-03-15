from __future__ import annotations

from typing import TYPE_CHECKING

from neoscore.core.graphic_object import GraphicObject
from neoscore.core.invisible_object import InvisibleObject
from neoscore.utils.point import Point

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class PathElement(InvisibleObject):
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
        parent: GraphicObject,
        control_1: ControlPoint,
        control_2: ControlPoint,
    ):
        super().__init__(pos, parent)
        self.control_1 = control_1
        self.control_2 = control_2
