from __future__ import annotations

from typing import Any, Optional, Union

from typing_extensions import TypeAlias

from neoscore.core.color import Color, ColorDef
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import ZERO, Unit
from neoscore.interface.pen_interface import PenInterface


class Pen:

    """A pen describing how shape outlines are drawn."""

    _default_color = Color("#000000")

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
                :obj:`.neoscore.set_default_color`.
            thickness: The stroke thickness. A value of ``ZERO`` (the default) indicates
                a display pixel width.
            pattern: The stroke pattern. Defaults to a solid line.
            join_style: The appearance of line joints. Defaults to a bevel join
            cap_style: The appearance of line ends. Defaults to a flat cap
        """
        if color is None:
            self._color = Pen._default_color
        else:
            self._color = Color.from_def(color)
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
        """Derive a pen from another, overriding any provided fields."""
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

    @classmethod
    def from_def(cls, pen_def: PenDef) -> Pen:
        if isinstance(pen_def, Pen):
            return pen_def
        else:
            return Pen(pen_def)

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
        """The color for the pen.

        This can be set with a :obj:`.ColorDef` shorthand."""
        return self._color

    @color.setter
    def color(self, value: ColorDef):
        self._color = Color.from_def(value)
        self._regenerate_interface()

    @property
    def thickness(self) -> Unit:
        """The pen stroke thickness."""
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
        """the style of unclosed path caps with this pen.

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


PenDef: TypeAlias = Union[Pen, str]
"""A ``Pen`` or a color hex string to be passed to an otherwise default ``Pen``."""
