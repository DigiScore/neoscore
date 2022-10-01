from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from PyQt5.QtWidgets import QGraphicsItem

from neoscore.core import neoscore
from neoscore.core.point import Point


@dataclass(frozen=True)
class GraphicObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from
    this and also be immutable dataclasses.
    """

    pos: Point
    """The absolute position of the object in canvas space."""

    parent: Optional[GraphicObjectInterface]
    """The object's parent, if any.

    If a parent interface is provided, it must be rendered before this interface.
    """

    scale: float
    """A scaling factor, where 1 is no scaling."""

    rotation: float
    """Rotation angle in degrees, where 0 is no rotation."""

    z_index: int
    """Z-index controlling draw order.

    Use 0 for the default draw order."""

    transform_origin: Point
    """The origin point for rotation and scaling transforms"""

    _qt_object: Optional[QGraphicsItem] = field(init=False, compare=False, repr=False)
    """A corresponding Qt object for internal use only.

    This value is set during rendering and is not meant to be set more than once.
    """

    def render(self):
        """Render the object to the scene.

        This is typically done by constructing a QGraphicsItem
        subclass and calling `_register_qt_object` with it.
        """
        raise NotImplementedError

    def _register_qt_object(self, obj: QGraphicsItem):
        neoscore.app_interface.scene.addItem(obj)
        super().__setattr__("_qt_object", obj)
