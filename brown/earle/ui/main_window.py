import os

from PyQt5 import QtWidgets, uic

from brown import config


class MainWindow(QtWidgets.QMainWindow):

    """The primary entry point for all UI code.

    This bootstraps the `main_window.ui` structure.
    """

    _ui_path = os.path.join(config.UI_DIR, 'main_window.ui')

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)

