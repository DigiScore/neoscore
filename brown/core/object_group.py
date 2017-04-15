from brown.core.invisible_object import InvisibleObject


class ObjectGroup(InvisibleObject):

    """An abstract collection of GraphicObjects."""

    def __init__(self, pos, parent=None, objects=None):
        """
        Args:
            pos (Point[Unit] or tuple): The local position
            parent (GraphicObject or None): The object's parent
            objects (set(GraphicObject)): The objects in the group.
        """
        super().__init__(pos, parent=parent)
        if objects:
            for child in objects:
                self._register_child(child)
