from brown.interface.invisible_object_interface import InvisibleObjectInterface
from brown.core.graphic_object import GraphicObject


class InvisibleObject(GraphicObject):

    _interface_class = InvisibleObjectInterface

    def __init__(self, pos, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            parent: The parent (core-level) object or None
        """
        # Hack? Initialize interface to position 0, 0
        # so that attribute setters don't try to push
        # changes to not-yet-existing interface
        self._interface = InvisibleObject._interface_class((0, 0))
        super().__init__(pos, 0, None, None, parent)

    def _render_complete(self):
        """Render the entire object.

        Returns: None
        """
        self._interface.render()
