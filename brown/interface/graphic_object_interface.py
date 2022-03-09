from dataclasses import dataclass

from brown.interface.brush_interface import BrushInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.point import Point


@dataclass(frozen=True)
class GraphicObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from
    this and also be immutable dataclasses.

    `GraphicObjectInterface` classes have no concept of parentage, or,
    by extension, page numbers. The `GraphicObject`s responsible for
    creating these interface objects should pass only document-space
    positions to these.
    """

    pos: Point
    """The absolute position of the object in canvas space."""

    pen: PenInterface

    brush: BrushInterface

    def render(self):
        """Render the object to the scene.

        This is typically done by constructing a QGraphicsItem
        subclass and adding it to the scene with
        `brown._app_interface.scene.addItem(qt_object)`.
        """
        raise NotImplementedError
