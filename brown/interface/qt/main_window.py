import os
from time import time

from PyQt5 import QtCore, QtWidgets, uic

QT_PRECISE_TIMER = 0
REFRESH_DELAY_MS = 15


class MainWindow(QtWidgets.QMainWindow):
    """The primary entry point for all UI code.

    This bootstraps the `main_window.ui` structure.
    """

    _ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)
        self.refresh_func = None

    def show(self):
        QtCore.QTimer.singleShot(REFRESH_DELAY_MS, QT_PRECISE_TIMER, self.refresh)
        super().show()

    @QtCore.pyqtSlot()
    def refresh(self):
        QtCore.QTimer.singleShot(REFRESH_DELAY_MS, QT_PRECISE_TIMER, self.refresh)
        if self.refresh_func:
            self.refresh_func(time())
