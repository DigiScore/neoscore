import os
from time import time

from PyQt5 import QtCore, QtWidgets, uic

from brown.constants import DEBUG

QT_PRECISE_TIMER = 0
REFRESH_DELAY_MS = 5


class MainWindow(QtWidgets.QMainWindow):
    """The primary entry point for all UI code.

    This bootstraps the `main_window.ui` structure.
    """

    _ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)
        self.refresh_func = None
        self._frame = 0  # Frame counter used in debug mode

    def show(self):
        QtCore.QTimer.singleShot(REFRESH_DELAY_MS, QT_PRECISE_TIMER, self.refresh)
        super().show()

    @QtCore.pyqtSlot()
    def refresh(self):
        QtCore.QTimer.singleShot(REFRESH_DELAY_MS, QT_PRECISE_TIMER, self.refresh)
        start_time = time()
        if self.refresh_func:
            self.refresh_func(start_time)
            if DEBUG:
                update_time = time() - start_time
                refresh_fps = int(1 / (time() - start_time))
                if self._frame % 30 == 0:
                    print(
                        f"Scene update took {int(update_time * 1000)} ms ({refresh_fps} / s)"
                    )
                self._frame += 1
