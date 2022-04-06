from dataclasses import dataclass, field

from PyQt5 import QtGui

from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.color import Color


@dataclass(frozen=True)
class BrushInterface:
    """Interface for a generic drawing brush controlling fill patterns."""

    color: Color
    pattern: BrushPattern
    qt_object: QtGui.QBrush = field(init=False)

    def __post_init__(self):
        color = QtGui.QColor(
            self.color.red, self.color.green, self.color.blue, self.color.alpha
        )
        q_brush = QtGui.QBrush(color, self.pattern.value)
        super().__setattr__("qt_object", q_brush)
