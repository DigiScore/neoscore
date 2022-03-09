from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point

if TYPE_CHECKING:
    from brown.core.mapping import Parent


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
        control_1: ControlPoint,
        control_2: ControlPoint,
        pos: Point,
        parent: GraphicObject,
    ):
        super().__init__(pos, parent)
        self.control_1 = control_1
        self.control_2 = control_2
