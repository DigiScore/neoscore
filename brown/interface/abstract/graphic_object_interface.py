from abc import ABC


class GraphicObjectInterface(ABC):
    """Interface for a generic graphic object.

    This is a top-level abstract interface class.
    """
    def __init__(self, parent, x, y, pen=None, brush=None):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """
        float: The x position of the Path relative to the document
        """
        raise NotImplementedError

    @x.setter
    def x(self, value):
        raise NotImplementedError

    @property
    def y(self):
        """
        float: The y position of the Path relative to the document
        """
        raise NotImplementedError

    @y.setter
    def y(self, value):
        raise NotImplementedError

    @property
    def pen(self):
        """
        PenInterface: The pen to draw outlines with
        """
        raise NotImplementedError

    @pen.setter
    def pen(self, value):
        raise NotImplementedError

    @property
    def brush(self):
        """
        BrushInterface: The brush to draw outlines with
        """
        raise NotImplementedError

    @brush.setter
    def brush(self, value):
        raise NotImplementedError

    @property
    def parent(self):
        """The interface of the parent object."""
        raise NotImplementedError

    @parent.setter
    def parent(self, value):
        raise NotImplementedError

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        raise NotImplementedError
