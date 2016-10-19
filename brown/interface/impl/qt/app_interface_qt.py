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
        self.current_brush = None

    def create_document(self, doctype='plane'):
        self.app = QtWidgets.QApplication([])
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

    def show(self):
        self.view.show()
        self.app.exec_()

    def set_pen(self, pen):
        """
        Set the current pen in the app

        Args:
            pen (PenInterface[Qt]): A pen interface object

        Returns: None
        """
        self.current_pen = pen

    def set_brush(self, brush):
        """
        Set the current brush in the app

        Args:
            brush (BrushInterface[Qt]): A brush interface object

        Returns: None
        """
        self.current_brush = brush

    def register_font(self, font_file_path):
        """
        Register a list of fonts to the graphics engine.

        Args:
            font_file_paths (strictly): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns: FontInterfaceQt: A newly created
            font interface object
        """
        font_id = QtGui.QFontDatabase.addApplicationFont(font_file_path)
        #family = QtGui.QFontDatabase.applicationFontFamilies(font_id).at(0)
