from brown.interface.invisible_object_interface import InvisibleObjectInterface
from brown.core.graphic_object import GraphicObject
from brown.utils.units import Unit


class InvisibleObject(GraphicObject):

    _interface_class = InvisibleObjectInterface

    def __init__(self, pos, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            parent: The parent object or None
        """
        super().__init__(pos, Unit(0), None, None, parent)

    def _render_complete(self, pos):
        interface = self._interface_class(pos)
        interface.render()
        self.interfaces.add(interface)
