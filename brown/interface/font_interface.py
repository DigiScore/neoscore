from PyQt5 import QtGui

from brown.core import brown
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import GraphicUnit


class UnknownFontFamilyError(Exception):
    """
    Exception raised when an invalid font name is passed to a FontInterface.
    """
    pass


class FontInterface:
    def __init__(self, family_name, size, weight=1, italic=False):
        """
        Args:
            family_name (str): The name of the font family
            size (float): The size of the font, in pixels
            weight (int): The font weight
            italic (bool): Italicized or not
        """
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self._qt_object = QtGui.QFont(self.family_name,
                                      self.size,
                                      self.weight,
                                      self.italic)
        self._qt_font_info_object = QtGui.QFontInfo(self._qt_object)
        self._qt_font_metrics_object = QtGui.QFontMetricsF(
            self._qt_object,
            brown._app_interface.view)

    ######## PUBLIC PROPERTIES ########

    @property
    def ascent(self):
        return self._qt_font_metrics_object.ascent()

    @property
    def descent(self):
        return self._qt_font_metrics_object.descent()

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font.

        REMINDER: Keep an eye on this. It's actually being calculated
        from the x-height of the font. Depending on the Qt specifics,
        this may or may not work as expected.
        """
        return GraphicUnit(self._qt_font_metrics_object.xHeight())

    ######## PUBLIC METHODS ########

    def tight_bounding_rect_around(self, text):
        """Calculate the tight bounding rectangle around a string in this font.

        Args:
            text (str): The text to calculate around.

        Returns:
            Rect[GraphicUnit]
        """
        qt_rect = self._qt_font_metrics_object.tightBoundingRect(text)
        return Rect(GraphicUnit(qt_rect.x()),
                    GraphicUnit(qt_rect.y()),
                    GraphicUnit(qt_rect.width()),
                    GraphicUnit(qt_rect.height()))
