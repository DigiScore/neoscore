from brown.interface.impl.qt import invisible_object_interface_qt
from brown.core.graphic_object import GraphicObject


class InvisibleObject(GraphicObject):

    _interface_class = invisible_object_interface_qt.InvisibleObjectInterfaceQt

    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            parent: The parent (core-level) object or None
        """
        # Hack? Initialize interface to position 0, 0
        # so that attribute setters don't try to push
        # changes to not-yet-existing interface
        self._interface = InvisibleObject._interface_class(0, 0)
        super().__init__(x, y, None, None, parent)
