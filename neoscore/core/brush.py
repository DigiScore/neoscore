from __future__ import annotations

from typing import Any, Optional, Union

from neoscore.core.brush_pattern import BrushPattern
from neoscore.interface.brush_interface import BrushInterface
from neoscore.utils.color import Color, ColorDef, color_from_def


class Brush:

    """A brush describing how shapes are filled in."""

    default_color = Color("#000000")

    def __init__(
        self,
        color: Optional[ColorDef] = None,
        pattern: BrushPattern = BrushPattern.SOLID,
    ):
        """
        Args:
            color: The brush color. Defaults to black unless changed globally by
                `neoscore.set_default_color`.
            pattern: The brush fill pattern.
        """
        if color is None:
            self._color = Brush.default_color
        else:
            self._color = color_from_def(color)
        self._pattern = pattern
        self._regenerate_interface()

    @classmethod
    def from_existing(
        cls,
        brush: Brush,
        color: Optional[ColorDef] = None,
        pattern: Optional[BrushPattern] = None,
    ) -> Brush:
        """Derive a Brush from another, overriding any provided fields."""
        return cls(color or brush.color, pattern or brush.pattern)

    @classmethod
    def no_brush(cls) -> Brush:
        """Create a non-drawing brush."""
        return Brush(pattern=BrushPattern.INVISIBLE)

    def _regenerate_interface(self):
        self._interface = BrushInterface(self.color, self.pattern)

    @property
    def color(self) -> Color:
        """The color for the brush"""
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self._regenerate_interface()

    @property
    def pattern(self) -> BrushPattern:
        """The fill pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value: BrushPattern):
        self._pattern = value
        self._regenerate_interface()

    @property
    def interface(self) -> BrushInterface:
        return self._interface

    def __eq__(self, other: Any) -> bool:
        """Brushes are compared by their attributes"""
        return (
            isinstance(other, Brush)
            and self.color == other.color
            and self.pattern == other.pattern
        )


SimpleBrushDef = Union[Brush, str]


def brush_from_simple_def(brush_def: SimpleBrushDef) -> Brush:
    if isinstance(brush_def, Brush):
        return brush_def
    else:
        return Brush(brush_def)
