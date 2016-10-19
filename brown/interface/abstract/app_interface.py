from abc import ABC


class AppInterface(ABC):

    def __init__(self):
        """
        TODO: Flesh out these docs
        """
        # Well defined function, not implemented
        raise NotImplementedError

    def create_document(self, doctype='plane'):
        # Well defined function, not implemented
        raise NotImplementedError

    def draw_line(self, x1, y1, x2, y2):
        # Well defined function, not implemented
        raise NotImplementedError

    def draw_circle(self, x, y, radius):
        # Well defined function, not implemented
        raise NotImplementedError

    def show(self):
        # Well defined function, not implemented
        raise NotImplementedError

    def set_pen(self, color, style):
        # Well defined function, not implemented
        raise NotImplementedError

    def set_color(self, color):
        # Well defined function, not implemented
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
