from __future__ import annotations

from typing import Any, Optional, Union

from typing_extensions import TypeAlias

from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.color import Color, ColorDef
from neoscore.interface.brush_interface import BrushInterface


class Brush:

    """A brush describing how shapes are filled in."""

    _default_color = Color("#000000")

    def __init__(
        self,
        color: Optional[ColorDef] = None,
        pattern: BrushPattern = BrushPattern.SOLID,
    ):
        """
        Args:
            color: The brush color. Defaults to black unless changed globally by
                ``neoscore.set_default_color``.
            pattern: The brush fill pattern.
        """
        if color is None:
            self._color = Brush._default_color
        else:
            self._color = Color.from_def(color)
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
    def from_def(cls, brush_def: BrushDef) -> Brush:
        if isinstance(brush_def, Brush):
            return brush_def
        else:
            return Brush(brush_def)

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


BrushDef: TypeAlias = Union[Brush, str]
"""A ``Brush`` or a color hex string to be passed to an otherwise default ``Brush``."""
