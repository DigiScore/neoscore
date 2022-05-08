"""Enums describing directions"""

from __future__ import annotations

from enum import Enum

from neoscore.core.units import Unit


class DirectionY(Enum):
    """A vertical direction"""

    UP = -1
    DOWN = 1

    def flip(self) -> DirectionY:
        """Return the opposite direction as this"""
        if self == DirectionY.UP:
            return DirectionY.DOWN
        else:
            return DirectionY.UP

    @classmethod
    def from_sign(cls, value: float | Unit) -> DirectionY:
        """Get a ``DirectionY`` from the sign of a number or ``Unit`` value."""
        if isinstance(value, Unit):
            sign = -1 if value.base_value < 0 else 1
        else:
            sign = -1 if value < 0 else 1
        if sign == -1:
            return DirectionY.UP
        else:
            return DirectionY.DOWN


class DirectionX(Enum):
    """A horizontal direction"""

    LEFT = -1
    RIGHT = 1

    def flip(self) -> DirectionX:
        """Return the opposite direction as this"""
        if self == DirectionX.LEFT:
            return DirectionX.RIGHT
        else:
            return DirectionX.LEFT

    @classmethod
    def from_sign(cls, value: float | Unit) -> DirectionX:
        """Get a ``DirectionX`` from the sign of a number or ``Unit`` value."""
        if isinstance(value, Unit):
            sign = -1 if value.base_value < 0 else 1
        else:
            sign = -1 if value < 0 else 1
        if sign == -1:
            return DirectionX.LEFT
        else:
            return DirectionX.RIGHT
