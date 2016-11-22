from brown.utils.point import Point
from brown.utils.graphic_unit import GraphicUnit
from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject


class PathElement(InvisibleObject):
    """A point with a parent to be use in Path objects.

    Although this is a GraphicObject, typically in practice they will be
    invisible.

    # TODO: Revisit and decide if this is a good way to go about this.
    """
    def __init__(self, path_element_interface, parent, parent_path):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                    relative to its parent
            parent (GraphicObject): The parent object or None
            parent_path (Path): The path this element belongs in
            path_element_interface (PathElementInterface): The interface
                for this element.
        """
        self._path_element_interface = path_element_interface
        super().__init__(self._path_element_interface.pos, parent=parent)
        self.parent_path = parent_path

    ######## PUBLIC PROPERTIES ########

    @property
    def element_type(self):
        """PathElementType: Enumeration for the type of element.

        This value is read-only.
        """
        return self._path_element_interface.element_type

    @property
    def pos(self):
        # Proxy for super getter so that setter can be extended.
        # return super().pos.fget(self)
        return self._pos

    @pos.setter
    def pos(self, value):
        # Use super setter, but also propogate change to interface
        # super().pos.fset(self, value)
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        self._interface.pos = self._pos
        self._path_element_interface.pos = value

    @property
    def x(self):
        # Proxy for super getter so that setter can be extended.
        # return super().x.fget(self)
        return self.pos.x

    @x.setter
    def x(self, value):
        # Use super setter, but also propogate change to interface
        # super().x.fset(self, value)
        self.pos.x = value
        self._interface.x = value
        self._path_element_interface.pos.x = value

    @property
    def y(self):
        # Proxy for super getter so that setter can be extended.
        # return super().y.fget(self)
        return self.pos.y

    @y.setter
    def y(self, value):
        # Use super setter, but also propogate change to interface
        # super().y.fset(self, value)
        self.pos.y = value
        self._interface.y = value
        self._path_element_interface.pos.y = value

    ######## PRIVATE METHODS ########

    def _update_element_interface_pos(self):
        """Sync this item's position with its interface item.

        If `self.parent == self.parent_path`, this will simply update the path
        element interface to `self.pos`.

        If `self.parent` is a GraphicObject different from the parent path,
        this maps the element's position to its position relative to the
        parent path.

        Returns: None
        """
        if self.parent == self.parent_path:
            self._path_element_interface.pos = self.pos
        else:
            self._path_element_interface.pos = self.pos_relative_to_item(
                self.parent_path)
