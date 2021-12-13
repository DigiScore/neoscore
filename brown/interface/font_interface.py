from PyQt5 import QtGui

from brown.core import brown
from brown.interface.interface import Interface
from brown.interface.qt.converters import qt_rect_to_rect
from brown.utils.units import GraphicUnit


class FontInterface(Interface):

    """An interface for fonts, exposing many font metadata properties."""

    def __init__(self, brown_object, family_name, size, weight, italic):
        """
        Args:
            brown_object (Brush): The object this interface belongs to
            family_name (str): The name of the font family
            size (Unit): The size of the font
            weight (int or None): The font weight. If `None`,
                a normal weight will be used.
            italic (bool): Italicized or not
        """
        super().__init__(brown_object)
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self.qt_object = QtGui.QFont(
            self.family_name,
            int(GraphicUnit(self.size).value),
            self.weight if self.weight is not None else -1,
            self.italic)
        self._qt_font_info_object = QtGui.QFontInfo(self.qt_object)
        self._qt_font_metrics_object = QtGui.QFontMetricsF(
            self.qt_object,
            brown._app_interface.view)

    ######## PUBLIC PROPERTIES ########

    @property
    def ascent(self):
        """GraphicUnit: The ascent of the font.

        The ascent is the vertical distance between the font baseline and
        the highest any font characters reach.
        """
        return GraphicUnit(self._qt_font_metrics_object.ascent())

    @property
    def descent(self):
        """GraphicUnit: The descent of the font.

        The ascent is the vertical distance between the font baseline and
        the lowest any font characters reach.
        """
        return GraphicUnit(self._qt_font_metrics_object.descent())

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font.

        NOTE: This is actually being calculated from the x-height of the font.
        Depending on the Qt specifics, this may or may not work as expected.
        """
        return GraphicUnit(self._qt_font_metrics_object.xHeight())

    ######## PUBLIC METHODS ########

    def bounding_rect_of(self, text):
        """Calculate the tight bounding rectangle around a string in this font.

        Args:
            text (str): The text to calculate around.

        Returns:
            Rect[GraphicUnit]
        """
        return qt_rect_to_rect(
            self._qt_font_metrics_object.tightBoundingRect(text),
            GraphicUnit)
