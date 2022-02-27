from dataclasses import dataclass

from brown.core.invisible_object import InvisibleObject
from brown.core.path_element_type import PathElementType
from brown.core.types import Parent
from brown.utils.point import Point


@dataclass(frozen=True)
class PathElement:

    pos: Point
    element_type: PathElementType
    parent: Parent

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y
