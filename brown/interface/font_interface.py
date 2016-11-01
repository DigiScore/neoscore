from PyQt5 import QtGui

from brown.core import brown


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
