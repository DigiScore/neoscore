from brown.interface.invisible_object_interface import InvisibleObjectInterface
from brown.core.graphic_object import GraphicObject


class MockGraphicObject(GraphicObject):

    """A mock GraphicObject subclass mostly for testing parentage."""

    _interface_class = InvisibleObjectInterface

    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            parent: The parent (core-level) object or None
        """
        self._interface = MockGraphicObject._interface_class(0, 0)
        super().__init__(x, y, None, None, parent)
