"""A naive benchmark for measuring the feasibility of animated scenes
using immutable data structures where the QT scene is reconstructed on
each frame.

Results here seem to indicate this is feasible, though `brown`
overhead would need to be minimal and frame rates would probably not
be consistently >60fps for complex scores.
"""


import os
import random
import time

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtPrintSupport import QPrinter

from brown.interface.qt.converters import point_to_qt_point_f
from brown.interface.qt.main_window import MainWindow
from brown.interface.qt.q_enhanced_text_item import QEnhancedTextItem
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class Window(MainWindow):
    def __init__(self):
        super().__init__()
        self.refresh_id = self.startTimer(33)

    def timerEvent(self, event):
        if event.timerId() == self.refresh_id:
            self.recreate_scene()

    def recreate_scene(self):
        start = time.time()
        self.graphicsView.scene().clear()

        for i in range(200):
            qt_object = QtWidgets.QGraphicsSimpleTextItem("test")
            x = GraphicUnit(random.randint(-500, 500))
            y = GraphicUnit(random.randint(-500, 500))
            qt_object.setPos(point_to_qt_point_f(Point(x, y)))
            self.graphicsView.scene().addItem(qt_object)
        print(f"updated scene in {time.time() - start} secs")


app = QtWidgets.QApplication([])

window = Window()

scene = QtWidgets.QGraphicsScene()
view = window.graphicsView
view.setScene(scene)
window.show()

app.exec_()
