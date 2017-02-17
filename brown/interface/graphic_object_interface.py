from abc import ABC

from brown.config import config
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface
from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.utils.color import Color
from brown.utils.stroke_pattern import StrokePattern


class GraphicObjectInterface(ABC):
    """Interface for a generic graphic object.

    This is a top-level abstract interface class.
    """
    def __init__(self, pos, pen=None, brush=None):
        """
        Must define and set:

            self._qt_object = # Some subclass of QGraphicsItem
            self.x = x
            self.y = y

        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point(GraphicUnit): The absolute position of the object."""
        return self._pos

    @pos.setter
    def pos(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        else:
            value = Point.from_existing(value)
        value.to_unit(GraphicUnit)
        self._pos = value
        self._qt_object.setX(self.pos.x.value)
        self._qt_object.setY(self.pos.y.value)

    @property
    def x(self):
        """GraphicUnit: The absolute x position of the object"""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = GraphicUnit(value)
        self._qt_object.setX(self.pos.x.value)

    @property
    def y(self):
        """GraphicUnit: The absolute y position of the object"""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = GraphicUnit(value)
        self._qt_object.setY(self.pos.y.value)

    @property
    def pen(self):
        """PenInterface: The pen to draw outlines with."""
        return self._pen

    @pen.setter
    def pen(self, value):
        # TODO: interface objects should really take a Pen as a mandatory arg,
        #       higher level classes should handle default values.
        if value:
            if isinstance(value, str):
                value = PenInterface(value)
            elif isinstance(value, PenInterface):
                pass
            else:
                raise TypeError
        else:
            value = PenInterface(Color(*config.DEFAULT_PEN_COLOR),
                                 GraphicUnit(config.DEFAULT_PEN_THICKNESS),
                                 StrokePattern(1))
        self._pen = value
        self._qt_object.setPen(self._pen._qt_object)

    @property
    def brush(self):
        """BrushInterface: The brush to fill shapes with"""
        return self._brush

    @brush.setter
    def brush(self, value):
        if value:
            if isinstance(value, str):
                value = BrushInterface(value)
            elif isinstance(value, BrushInterface):
                pass
            else:
                raise TypeError
        else:
            value = BrushInterface(Color(*config.DEFAULT_BRUSH_COLOR))
        self._brush = value
        self._qt_object.setBrush(self._brush._qt_object)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
