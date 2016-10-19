from abc import ABC


class AppInterface(ABC):

    def __init__(self):
        """
        TODO: Flesh out these docs
        """
        # TODO: Doc me!
        raise NotImplementedError

    def create_document(self, doctype='plane'):
        # TODO: Doc me!
        raise NotImplementedError

    def show(self):
        # TODO: Doc me!
        raise NotImplementedError

    def set_pen(self, pen):
        """
        Set the current pen in the app

        Args:
            pen (PenInterface[Qt]): A pen interface object

        Returns: None
        """
        raise NotImplementedError

    def set_brush(self, brush):
        """
        Set the current brush in the app

        Args:
            brush (BrushInterface[Qt]): A brush interface object

        Returns: None
        """
        raise NotImplementedError

    def register_font(self, font_file_path):
        """
        Register a list of fonts to the graphics engine.

        Args:
            font_file_paths (strictly): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns: FontInterface (implementation): A newly created
            font interface object
        """
        raise NotImplementedError
