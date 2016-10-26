from abc import ABC


class InvisibleObjectInterface(ABC):
    """
    Interface for a non-drawing object with a position, parent, and children.
    """
    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the parent.
            y (float): The y position of the path relative to the parent.
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
    def parent(self):
        """The interface of the parent object."""
        raise NotImplementedError

    @parent.setter
    def parent(self, value):
        raise NotImplementedError
