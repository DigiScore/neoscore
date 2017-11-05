from brown.interface.interface import Interface
from brown.interface.qt.converters import point_to_qt_point_f
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class GraphicObjectInterface(Interface):
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from this.

    `GraphicObjectInterface` classes have no concept of parentage, or,
    by extension, page numbers. The `GraphicObject`s responsible for
    creating these interface objects should pass only document-space
    positions to these.

    Implementing class `__init__` methods should, in the following order:
    * Create a `QGraphicsItem` subclass object and store it in
      `self.qt_object`.
    * Set `self.pos`, `self.pen`, and `self.brush`. The setters
      will automatically update `self.qt_object` with their values
      translated into Qt-compatible values.
    """

    def __init__(self, brown_object):
        """
        Args:
            brown_object (GraphicObject): the brown object this belongs to
        """
        super().__init__(brown_object)

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point[Unit]: The absolute position of the object.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._pos

    @pos.setter
    def pos(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        else:
            value = Point.from_existing(value)
        self._pos = value
        self.qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def x(self):
        """Unit: The absolute x position of the object

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value
        self.qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def y(self):
        """Unit: The absolute y position of the object

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = GraphicUnit(value)
        self.qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def pen(self):
        """PenInterface: The pen to draw outlines with.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        self.qt_object.setPen(self._pen.qt_object)

    @property
    def brush(self):
        """BrushInterface: The brush to fill shapes with.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        self.qt_object.setBrush(self._brush.qt_object)

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
