from brown.core.invisible_object import InvisibleObject
from brown.utils.path_element_type import PathElementType


class PathElement(InvisibleObject):
    """A point with a parent to be use in Path objects.

    Although this is a GraphicObject, typically in practice they will be
    invisible.
    """
    def __init__(self, pos, element_type, path, parent=None):
        """
        Args:
            pos (Point[Unit]): The position of the element relative to its parent
            element_type (PathElementType or int): The type of the element
            path (Path): The path this element belongs in
            parent (GraphicObject): The parent object. If None, the parent
                will be the path.
        """
        super().__init__(pos, parent=parent)
        self.parent_path = path
        self.element_type = element_type

    ######## PUBLIC PROPERTIES ########

    @property
    def element_type(self):
        """PathElementType: Enumeration for the type of element.

        This value is read-only.
        """
        return self._element_type
        return self._path_element_interface.element_type

    @element_type.setter
    def element_type(self, value):
        self._element_type = PathElementType(value)
