from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.interface.abstract.app_interface import AppInterface


class AppInterfaceQt(AppInterface):

    def __init__(self):
        # implementation of api specified in AppInterface
        print('Initializing with QT toolkit')
        self.app = None
        self.scene = None
        self.current_pen = None
        self.default_pen = QtGui.QPen()
        self.color = None

    def create_document(self, doctype='plane'):
        self.app = QtWidgets.QApplication([])
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

    def show(self):
        self.view.show()
        self.app.exec_()

    def set_pen(self, color, style):
        self.current_pen = QtGui.QPen()

    def set_color(self, color):
        # Well defined function, not implemented
        self.color = QtGui.QBrush(QtGui.QColor(color),
                                  11)  # 0: no fill
