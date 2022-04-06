from dataclasses import dataclass, field

from PyQt5 import QtGui

from neoscore.core.color import Color
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Unit


@dataclass(frozen=True)
class PenInterface:
    """Interface for a pen controlling path outline appearance."""

    color: Color

    thickness: Unit
    """The pen thickness. If zero, a cosmetic pixel thickness is used."""

    pattern: PenPattern

    join_style: PenJoinStyle

    cap_style: PenCapStyle

    qt_object: QtGui.QPen = field(init=False)

    def __post_init__(self):
        color = QtGui.QColor(
            self.color.red, self.color.green, self.color.blue, self.color.alpha
        )
        brush = QtGui.QBrush(color)
        q_pen = QtGui.QPen(
            brush,
            self.thickness.base_value,
            self.pattern.value,
            self.cap_style.value,
            self.join_style.value,
        )
        super().__setattr__("qt_object", q_pen)
