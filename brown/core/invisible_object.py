from brown.interface.impl.qt import invisible_object_interface_qt



class InvisibleObject:

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
        self.x = x
        self.y = y
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """
        float: The x position of the Path relative to the document
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._interface.x = value

    @property
    def y(self):
        """
        float: The y position of the Path relative to the document
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._interface.y = value

    @property
    def parent(self):
        """The parent object"""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            self._interface.parent = value._interface
        else:
            self._interface.parent = None
