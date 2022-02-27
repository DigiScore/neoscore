from __future__ import annotations

from typing import Protocol, Union

from brown.core.graphic_object import GraphicObject
from brown.core.page import Page
from brown.utils.point import Point

Parent = Union[GraphicObject, Page]


class Positioned(Protocol):
    def pos(self) -> Point:
        ...

    def parent(self) -> Union[Positioned, Page]:
        ...
