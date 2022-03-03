import os
from time import time

from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    """The primary entry point for all UI code.

    This bootstraps the `main_window.ui` structure.
    """

    _ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)
        self.refresh_timer_id = None
        self.refresh_func = None

    def show(self):
        self.refresh_timer_id = self.startTimer(10)
        super().show()

    def timerEvent(self, event):
        if event.timerId() == self.refresh_timer_id and self.refresh_func:
            self.refresh_func(time())
