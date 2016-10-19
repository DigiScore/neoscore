from abc import ABC


class AppInterface(ABC):
    """The primary interface to the application state.

    This holds much of the global state for interacting with the API,
    and must be created (and `create_document()` must be called) before
    working with the API.
    """

    def __init__(self):
        raise NotImplementedError

    def create_document(self, doctype='plane'):
        """Initialize a document.

        This is required before just about any operation
        in the API can be performed.
        """
        raise NotImplementedError

    def show(self):
        """Open a window showing a preview of the document."""
        raise NotImplementedError

    def set_pen(self, pen):
        """Set the current pen in the app.

        Args:
            pen (PenInterface): A pen interface object

        Returns: None
        """
        raise NotImplementedError

    def set_brush(self, brush):
        """Set the current brush in the app

        Args:
            brush (BrushInterface): A brush interface object

        Returns: None
        """
        raise NotImplementedError

    def register_font(self, font_file_path):
        """Register a list of fonts to the graphics engine.

        Args:
            font_file_paths (strictly): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns: FontInterface (implementation): A newly created
            font interface object
        """
        raise NotImplementedError
