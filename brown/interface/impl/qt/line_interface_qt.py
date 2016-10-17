from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.line_interface import LineInterface


class LineInterfaceQt(LineInterface):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, color=None, pattern=None):
        brown._app_interface.scene.addLine(self.x1, self.y1,
                                           self.x2, self.y2,
                                           brown._app_interface.default_pen)
