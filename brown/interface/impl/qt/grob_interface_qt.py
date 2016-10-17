from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.grob_interface import GrobInterface


class GrobInterfaceQt(GrobInterface):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        brown._app_interface.scene.addLine(0, 0, self.x, self.y,
                                           brown._app_interface.default_pen)
