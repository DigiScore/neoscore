from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class AppInterface:
    """The primary interface to the application state.

    This holds much of the global state for interacting with the API,
    and must be created (and `create_document()` must be called) before
    working with the API.
    """

    def __init__(self):
        self.app = None
        self.scene = None
        self.current_pen = None
        self.current_brush = None

    def create_document(self, doctype='plane'):
        """Initialize a document.

        This is required before just about any operation
        in the API can be performed.
        """
        self.app = QtWidgets.QApplication([])
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

    def show(self):
        """Open a window showing a preview of the document."""
        print('Launching Qt Application instance')
        self.view.show()
        self.app.exec_()

    def destroy(self):
        """Destroy the window and all global interface-level data."""
        print('Tearing down Qt Application instance')
        self.app.exit()
        self.app = None
        self.scene = None
        self.current_pen = None
        self.current_brush = None

    def set_pen(self, pen):
        """Set the current pen in the app

        Args:
            pen (PenInterfaceQt): A pen interface object

        Returns: None
        """
        self.current_pen = pen

    def set_brush(self, brush):
        """Set the current brush in the app

        Args:
            brush (BrushInterfaceQt): A brush interface object

        Returns: None
        """
        self.current_brush = brush

    def register_font(self, font_file_path):
        """Register a list of fonts to the graphics engine.

        Args:
            font_file_paths (strictly): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns: FontInterfaceQt: A newly created
            font interface object
        """
        font_id = QtGui.QFontDatabase.addApplicationFont(font_file_path)
        if font_id == -1:
            print('FONT LOADED FROM {} RETURNED ID OF {}'.format(
                font_file_path, font_id))
        #family = QtGui.QFontDatabase.applicationFontFamilies(font_id).at(0)
