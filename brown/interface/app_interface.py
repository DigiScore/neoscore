from PyQt5 import QtWidgets
from PyQt5 import QtGui


class FontRegistrationError(Exception):
    """Exception raised when a font is loaded from disk unsuccessfully."""
    pass


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

    ######## PUBLIC PROPERTIES ########

    @property
    def current_pen(self):
        """PenInterface: The current pen for certain default drawing

        # TODO: Which objects are affected by this? Is this even needed?
        """
        return self._current_pen

    @current_pen.setter
    def current_pen(self, value):
        self._current_pen = value

    @property
    def current_brush(self):
        """BrushInterface: The current brush for certain default drawing

        # TODO: Which objects are affected by this? Is this even needed?
        """
        return self._current_brush

    @current_brush.setter
    def current_brush(self, value):
        self._current_brush = value

    ######## PUBLIC METHODS ########

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

    def register_font(self, font_file_path):
        """Register a list of fonts to the graphics engine.

        Args:
            font_file_paths (str): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns:
            int: The id of the newly registered font
            TODO: Investigate more if returning an ID is really
                  the thing to do here...
        """
        font_id = QtGui.QFontDatabase.addApplicationFont(font_file_path)
        if font_id == -1:
            raise FontRegistrationError(
                'Font loaded from {} failed'.format(font_file_path))
        print("Font registered with ID {}".format(font_id))
        return font_id
        #family = QtGui.QFontDatabase.applicationFontFamilies(font_id).at(0)
