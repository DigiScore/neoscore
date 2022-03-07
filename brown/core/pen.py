from __future__ import annotations

from brown import constants
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.units import GraphicUnit, Unit


class Pen:
    """Class for a generic drawing pen controlling fill patterns.

    Currently only solid colors are supported.
    """

    def __init__(
        self,
        color="#000000",
        thickness=None,
        pattern=PenPattern.SOLID,
        join_style=PenJoinStyle.BEVEL,
        cap_style=PenCapStyle.SQUARE,
    ):
        """
        Args:
            color (Color or init tuple): The stroke color
            thickness (Unit): The stroke thickness.
                A value of `0` indicates Args cosmetic pixel width.
                Defaults to `constants.DEFAULT_PEN_THICKNESS`.
            pattern (PenPattern): The stroke pattern.
                Defaults to a solid line.
            join_style (PenJoinStyle): Defaults to a bevel join
            cap_style (PenCapStyle): Defaults to a square cap

        """
        if isinstance(color, Color):
            self._color = color
        elif isinstance(color, tuple):
            self._color = Color(*color)
        else:
            self._color = Color(color)
        self._thickness = (
            thickness
            if thickness is not None
            else GraphicUnit(constants.DEFAULT_PEN_THICKNESS)
        )
        self._pattern = pattern
        self._join_style = join_style
        self._cap_style = cap_style
        self._regenerate_interface()

    @classmethod
    def from_existing(cls, pen: Pen) -> Pen:
        """Clone a pen."""
        return cls(pen.color, pen.thickness, pen.pattern, pen.join_style, pen.cap_style)

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


NO_PEN = Pen(pattern=PenPattern.NO_PEN)
