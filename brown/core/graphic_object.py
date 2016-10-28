from abc import ABC


class GraphicObject:
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.
    """
    def __init__(self, x, y, pen=None, brush=None, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent (core-level) object or None
        """
        self.x = x
        self.y = y
        self.pen = pen
        self.brush = brush
        self.parent = parent

    ######## PRIVATE PROPERTIES ########

    @property
    def __interface(self):
        """The interface layer object responsible for rendering"""
        return self._interface

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
    def pen(self):
        """
        Pen: The pen to draw outlines with
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._pen:
            self._interface.pen = self._pen._interface

    @property
    def brush(self):
        """
        Brush: The brush to draw outlines with
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._brush:
            self._interface.brush = self._brush._interface

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

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        self._interface.render()
