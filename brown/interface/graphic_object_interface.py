from dataclasses import dataclass

from PyQt5.QtWidgets import QGraphicsItem

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


@dataclass(frozen=True)
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

    # TODO MEDIUM update above docs on new implementation pattern

    pos: Point
    """The absolute position of the object in canvas space."""

    pen: PenInterface

    brush: BrushInterface

    def render(self):
        """Render the object to the scene."""
        raise NotImplementedError

    def _create_qt_object(self) -> QGraphicsItem:
        """Create a Qt object corresponding to this interface's attributes"""
        raise NotImplementedError
