from __future__ import annotations

from enum import Enum

from neoscore.core.units import Unit


class VerticalDirection(Enum):
    UP = -1
    DOWN = 1

    def flip(self):
        if self == VerticalDirection.UP:
            return VerticalDirection.DOWN
        else:
            return VerticalDirection.UP

    @classmethod
    def from_sign(cls, value: float | Unit) -> VerticalDirection:
        """Get a VerticalDirection from the sign of a number or `Unit` value."""
        if isinstance(value, Unit):
            sign = -1 if value.base_value < 0 else 1
        else:
            sign = -1 if value < 0 else 1
        if sign == -1:
            return VerticalDirection.UP
        else:
            return VerticalDirection.DOWN


class HorizontalDirection(Enum):
    LEFT = -1
    RIGHT = 1

    def flip(self):
        if self == HorizontalDirection.LEFT:
            return HorizontalDirection.RIGHT
        else:
            return HorizontalDirection.LEFT

    @classmethod
    def from_sign(cls, value: float | Unit) -> HorizontalDirection:
        """Get a HorizontalDirection from the sign of a number or `Unit` value."""
        if isinstance(value, Unit):
            sign = -1 if value.base_value < 0 else 1
        else:
            sign = -1 if value < 0 else 1
        if sign == -1:
            return HorizontalDirection.LEFT
        else:
            return HorizontalDirection.RIGHT
