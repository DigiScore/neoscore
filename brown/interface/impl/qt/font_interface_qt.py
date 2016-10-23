from PyQt5 import QtGui

from brown.interface.abstract.font_interface import FontInterface
from brown.core import brown


class FontInterfaceQt(FontInterface):
    def __init__(self, family_name, size, weight=1, italic=False):
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self._qt_object = QtGui.QFont(self.family_name,
                                      self.size,
                                      self.weight,
                                      self.italic)
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
