from brown.interface.brush_interface import BrushInterface
from brown.interface.pen_interface import PenInterface
from brown.interface.qt.converters import point_to_qt_point_f
from brown.utils.point import Point
from brown.utils.units import GraphicUnit

# TODO HIGH should at least GraphicObject interfaces generally be
# immutable?  right now they create and mutate a qt object as they're
# constructed, but this could be rearranged so each GOI class
# implements a `create_qt_object` method which constructs and sets up
# in one go. that would simplify a lot of code.


class GraphicObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from this.

    `GraphicObjectInterface` classes have no concept of parentage, or,
    by extension, page numbers. The `GraphicObject`s responsible for
    creating these interface objects should pass only document-space
    positions to these.

    Implementing class `__init__` methods should, in the following order:
    * Call `super().__init__()`
    * Create a `QGraphicsItem` subclass object and store it in
      `self.qt_object`.
    * Set `self.pos`, `self.pen`, and `self.brush`. The setters
      will automatically update `self.qt_object` with their values
      translated into Qt-compatible values.
    """

    def __init__(self):
        self._pos = None
        self._pen = None
        self._brush = None
        self.qt_object = None

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self) -> Point:
        """Point: The absolute position of the object.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._pos

    @pos.setter
    def pos(self, value: Point):
        self._pos = value
        self.qt_object.setPos(point_to_qt_point_f(self.pos))

    @property
    def pen(self) -> PenInterface:
        """PenInterface: The pen to draw outlines with.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._pen

    @pen.setter
    def pen(self, value: PenInterface):
        self._pen = value
        self.qt_object.setPen(self._pen.qt_object)

    @property
    def brush(self) -> BrushInterface:
        """BrushInterface: The brush to fill shapes with.

        This setter automatically propagates changes to
        the underlying Qt object.
        """
        return self._brush

    @brush.setter
    def brush(self, value: BrushInterface):
        self._brush = value
        self.qt_object.setBrush(self._brush.qt_object)

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
