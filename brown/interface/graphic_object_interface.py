from abc import ABC

from brown.interface.qt_to_util import point_to_qt_point_f
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class GraphicObjectInterface(ABC):
    """Interface for a generic graphic object.

    This is a top-level abstract interface class. All graphic interfaces
    for renderable objects should descend from this.

    `GraphicObjectInterface` classes have no concept of parentage, or,
    by extension, page numbers. The `GraphicObject`s responsible for
    creating these interface objects should pass only document-space
    positions to these.
    """
    def __init__(self):
        """
        This method should (in this order):
        1) Create a QGraphicsItem subclass object and store it in
           self._qt_object
        2) Set the following properties:
           a) self.pos
           b) self.pen
           c) self.brush
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point[Unit]: The absolute position of the object."""
        return self._pos

    @pos.setter
    def pos(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        else:
            value = Point.from_existing(value)
        self._pos = value
        self._qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def x(self):
        """Unit: The absolute x position of the object"""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value
        self._qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def y(self):
        """Unit: The absolute y position of the object"""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = GraphicUnit(value)
        self._qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def pen(self):
        """PenInterface: The pen to draw outlines with."""
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        self._qt_object.setPen(self._pen._qt_object)

    @property
    def brush(self):
        """BrushInterface: The brush to fill shapes with."""
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        self._qt_object.setBrush(self._brush._qt_object)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
