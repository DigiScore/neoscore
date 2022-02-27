from __future__ import annotations

from typing import Protocol, Union, runtime_checkable

from brown.core.page import Page
from brown.utils.point import Point


@runtime_checkable
class Positioned(Protocol):
    @property
    def pos(self) -> Point:
        ...

    @property
    def parent(self) -> Positioned:
        ...
