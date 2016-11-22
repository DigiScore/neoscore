from abc import ABC

from brown.utils.units import GraphicUnit
from brown.utils.point import Point


class GraphicObject(ABC):
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.
    """
    def __init__(self, pos, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                relative to its parent
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        self.pos = pos
        self.pen = pen
        self.brush = brush
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The starting point of the frame on the first page."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        self._interface.pos = self._pos

    @property
    def x(self):
        """
        GraphicUnit: The x position of the Path relative to the document
        """
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value
        self._interface.x = value

    @property
    def y(self):
        """
        GraphicUnit: The y position of the Path relative to the document
        """
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value
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

    def pos_relative_to_item(self, other):
        """Find this object's position relative to another GraphicObject

        Args:
            other (GraphicObject): The object to map from

        Returns: Point
        """
        if self.parent == other:
            return self.pos
        return self._interface.pos_relative_to_item(other._interface)

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        self._interface.render()

    ######## PRIVATE METHODS ########

    def _render_before_break(self, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None
        """
        raise NotImplementedError

    def _render_after_break(self, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None
        """
        raise NotImplementedError

    def _render_spanning_continuation(self, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that
        crosses two breaks. This function should render the
        portion of the object surrounded by breaks on either side.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None
        """
        raise NotImplementedError
