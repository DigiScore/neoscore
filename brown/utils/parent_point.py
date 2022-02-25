from __future__ import annotations

from typing import NamedTuple, Optional, Type, Union

from brown.core.types import Parent
from brown.utils.point import Point
from brown.utils.units import Unit


class ParentPoint(NamedTuple):
    """A point with an optional parent.

    This behaves similarly to `Point`, but its magic methods work only
    between other `ParentPoint`s which share a parent.

    Care should be taken, assisted by type checkers where possible,
    to not mix ParentPoints up with Points. In some situations duck
    typing may allow some interoperability with counterintuitive
    results.
    """

    x: Unit
    y: Unit
    parent: Optional[Parent] = None

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def from_point(cls, point: Point, parent: Optional[Parent]):
        """Create a `ParentPoint` from an existing `Point` and a parent."""
        return cls(point.x, point.y, parent)

    ######## SPECIAL METHODS ########

    def __add__(self, other: ParentPoint):
        if type(other) != ParentPoint:
            raise TypeError
        if self.parent != other.parent:
            raise AttributeError("Cannot add ParentPoints with different parents")
        return ParentPoint(self.x + other.x, self.y + other.y, self.parent)

    def __sub__(self, other: ParentPoint):
        if type(other) != ParentPoint:
            raise TypeError
        if self.parent != other.parent:
            raise AttributeError("Cannot add ParentPoints with different parents")
        return ParentPoint(self.x - other.x, self.y - other.y, self.parent)

    def __mul__(self, other: float):
        try:
            return ParentPoint(self.x * other, self.y * other, self.parent)
        except AttributeError:
            raise TypeError

    ######## PUBLIC METHODS ########

    def in_unit(self, unit: Type[Unit]) -> ParentPoint:
        return ParentPoint(unit(self.x), unit(self.y), self.parent)
