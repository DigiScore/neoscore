from dataclasses import dataclass, field
from typing import Optional

from PyQt5 import QtGui

from neoscore.core import neoscore
from neoscore.core.rect import Rect
from neoscore.core.units import Unit
from neoscore.interface.qt.converters import qt_rect_to_rect


@dataclass(frozen=True)
class FontInterface:

    """An interface for fonts, exposing some commonly used metadata."""

    family_name: str
    size: Unit
    weight: Optional[int]
    italic: bool

    ascent: Unit = field(init=False)
    """The ascent of the font.

    The ascent is the vertical distance between the font baseline and
    the highest any font characters reach.
    """

    descent: Unit = field(init=False)
    """The descent of the font.

    The ascent is the vertical distance between the font baseline and
    the lowest any font characters reach.
    """

    x_height: Unit = field(init=False)
    """The x-height for the font.

    This is generally similar, if not identical, to the em size.
    """

    qt_object: QtGui.QFont = field(init=False)

    _qt_font_info_object: QtGui.QFontInfo = field(init=False)
    _qt_font_metrics_object: QtGui.QFontMetricsF = field(init=False)

    def __post_init__(self):
        super().__setattr__(
            "qt_object",
            QtGui.QFont(
                self.family_name,
                # Float font sizes can't be set in QFont's constructor,
                # so set it to -1 (system default) here and set actual
                # size below with setPointSizeF
                -1,
                self.weight if self.weight is not None else -1,
                self.italic,
            ),
        )
        self.qt_object.setPixelSize(round(self.size.base_value))
        super().__setattr__("_qt_font_info_object", QtGui.QFontInfo(self.qt_object))
        super().__setattr__(
            "_qt_font_metrics_object",
            QtGui.QFontMetricsF(self.qt_object, neoscore.app_interface.view),
        )
        super().__setattr__("ascent", Unit(self._qt_font_metrics_object.ascent()))
        super().__setattr__("descent", Unit(self._qt_font_metrics_object.descent()))

        super().__setattr__("x_height", Unit(self._qt_font_metrics_object.xHeight()))

    def bounding_rect_of(self, text: str) -> Rect:
        """Calculate the tight bounding rectangle around a string in this font."""
        # Qt warns that tightBoundingRect is very slow on Windows.
        # Maybe horizontalAdvance can be used instead?
        return qt_rect_to_rect(self._qt_font_metrics_object.tightBoundingRect(text))
