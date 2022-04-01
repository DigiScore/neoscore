from __future__ import annotations

from typing import Any, Optional, Union

from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.interface.pen_interface import PenInterface
from neoscore.utils.color import Color, ColorDef, color_from_def
from neoscore.utils.units import ZERO, Unit


class Pen:

    """A pen describing how shape outlines are drawn."""

    default_color = Color("#000000")

    def __init__(
        self,
        color: Optional[ColorDef] = None,
        thickness: Optional[Unit] = ZERO,
        pattern: PenPattern = PenPattern.SOLID,
        join_style: PenJoinStyle = PenJoinStyle.MITER,
        cap_style: PenCapStyle = PenCapStyle.FLAT,
    ):
        """
        Args:
            color: The stroke color. Defaults to black unless changed globally by
                `neoscore.set_default_color`.
            thickness: The stroke thickness. A value of `0` (the default) indicates
                a display pixel width.
            pattern: The stroke pattern. Defaults to a solid line.
            join_style: Defaults to a bevel join
            cap_style: Defaults to a square cap
        """
        if color is None:
            self._color = Pen.default_color
        else:
            self._color = color_from_def(color)
        self._thickness = thickness
        self._pattern = pattern
        self._join_style = join_style
        self._cap_style = cap_style
        self._regenerate_interface()

    @classmethod
    def from_existing(
        cls,
        pen: Pen,
        color: Optional[ColorDef] = None,
        thickness: Optional[Unit] = None,
        pattern: Optional[PenPattern] = None,
        join_style: Optional[PenJoinStyle] = None,
        cap_style: Optional[PenCapStyle] = None,
    ) -> Pen:
        """Derive a Pen from another, overriding any provided fields."""
        return cls(
            color or pen.color,
            thickness or pen.thickness,
            pattern or pen.pattern,
            join_style or pen.join_style,
            cap_style or pen.cap_style,
        )

    @classmethod
    def no_pen(cls) -> Pen:
        """Create a non-drawing pen."""
        return Pen(pattern=PenPattern.INVISIBLE)

    def _regenerate_interface(self):
        self._interface = PenInterface(
            self.color,
            self.thickness,
            self.pattern,
            self.join_style,
            self.cap_style,
        )

    @property
    def color(self) -> Color:
        """The color for the pen"""
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self._regenerate_interface()

    @property
    def thickness(self) -> Unit:
        """The stroke thickness."""
        return self._thickness

    @thickness.setter
    def thickness(self, value: Unit):
        self._thickness = value
        self._regenerate_interface()

    @property
    def pattern(self) -> PenPattern:
        """The stroke pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, value: PenPattern):
        self._pattern = value
        self._regenerate_interface()

    @property
    def join_style(self) -> PenJoinStyle:
        """The style of line sharp line joins.

        This style has no effect on curved paths.
        """
        return self._join_style

    @join_style.setter
    def join_style(self, value: PenJoinStyle):
        self._join_style = value
        self._regenerate_interface()

    @property
    def cap_style(self) -> PenCapStyle:
        """PenCapStyle: the style of unclosed path caps with this pen.

        This style has no effect on closed paths."""
        return self._cap_style

    @cap_style.setter
    def cap_style(self, value: PenCapStyle):
        self._cap_style = value
        self._regenerate_interface()

    @property
    def interface(self) -> PenInterface:
        return self._interface

    def __eq__(self, other: Any) -> bool:
        """Pens are compared by their attributes"""
        return (
            isinstance(other, Pen)
            and self.color == other.color
            and self.thickness == other.thickness
            and self.pattern == other.pattern
            and self.join_style == other.join_style
            and self.cap_style == other.cap_style
        )


SimplePenDef = Union[Pen, str]
"""A pen or a color hex string to be passed to an otherwise default `Pen`."""


# TODO high move into Pen


def pen_from_simple_def(pen_def: SimplePenDef) -> Pen:
    if isinstance(pen_def, Pen):
        return pen_def
    else:
        return Pen(pen_def)
