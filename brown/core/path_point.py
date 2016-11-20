from brown.utils.point import Point
from brown.core.invisible_object import InvisibleObject


class PathPoint(InvisibleObject):
    """A point with a parent to be use in Path objects.

    Although this is a GraphicObject, typically in practice they will be
    invisible.

    # TODO: Revisit and decide if this is a good way to go about this.
    """
    def __init__(self, pos, parent):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                    relative to its parent
            parent (GraphicObject): The parent object or None
        """
        super().__init__(pos, parent=parent)
