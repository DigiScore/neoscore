from brown.interface.abstract.graphic_object_interface import GraphicObjectInterface


class InvisibleObjectInterface(GraphicObjectInterface):
    """
    Interface for a non-drawing object with a position, parent, and children.
    """
    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the parent.
            y (float): The y position of the path relative to the parent.
            parent (GraphicObjectInterface): The parent of the object
        """
        raise NotImplementedError
