from brown.core.invisible_object import InvisibleObject
from brown.core.path_element_type import PathElementType
from brown.core.types import Parent
from brown.utils.point import Point


class PathElement(InvisibleObject):
    """A point with a parent to be use in Path objects.

    Although this is a GraphicObject, typically in practice they will be
    invisible.
    """

    def __init__(self, pos: Point, element_type: PathElementType, parent: Parent):
        """
        Args:
            pos (Point): The position of the element relative to its parent
            element_type (PathElementType or int): The type of the element
            path (Path): The path this element belongs in
            parent (GraphicObject): The parent object. This will often be the
                owning path, but in cases where a path element is anchored to a
                separate object, this may be that object.
        """
        super().__init__(pos, parent=parent)
        self._element_type = element_type

    ######## PUBLIC PROPERTIES ########

    @property
    def element_type(self):
        """PathElementType: Enumeration for the type of element."""
        return self._element_type

    @element_type.setter
    def element_type(self, value):
        self._element_type = value

    # TODO I believe eq and hash should not be allowed on path
    # elements since they're GraphicObjects which are mutable and have
    # lots of other properties not checked here.

    def __eq__(self, other):
        return (
            type(other) == PathElement
            and self.pos == other.pos
            and self.parent == other.parent
            and self.element_type == other.element_type
        )

    def __hash__(self):
        return hash(self.pos) ^ hash(self.parent) ^ hash(self.element_type)
