from dataclasses import dataclass

from neoscore.core.point import Point


@dataclass(frozen=True)
class PositionedObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from
    this and also be immutable dataclasses.

    ``PositionedObjectInterface`` classes have no concept of parentage, or, by
    extension, page numbers. Objects creating these interfaces should pass only
    document-space positions to these.
    """

    pos: Point
    """The absolute position of the object in canvas space."""

    def render(self):
        """Render the object to the scene.

        This is typically done by constructing a QGraphicsItem
        subclass and adding it to the scene with
        ``neoscore._app_interface.scene.addItem(qt_object)``.
        """
        raise NotImplementedError
