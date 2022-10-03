from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from warnings import warn

from PyQt5.QtWidgets import QGraphicsItem

from neoscore.core import neoscore
from neoscore.core.point import Point


@dataclass(frozen=True)
class PositionedObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from
    this and also be immutable dataclasses.
    """

    pos: Point
    """The position of the object.

    If a parent is provided, this position is relative to that interface. Otherwise it
    is in absolute document coordinates.
    """

    parent: Optional[PositionedObjectInterface]
    """The object's parent, if any.

    If a parent interface is provided, it must be rendered before this interface.
    """

    scale: float
    """A scaling factor, where 1 is no scaling.

    This occurs relative to ``transform_origin``.

    Scaling is inherited from parents to children along the interface tree.
    """

    rotation: float
    """Rotation angle in degrees, where 0 is no rotation.

    This occurs relative to ``transform_origin``.

    Rotation is inherited from parents to children along the interface tree.
    """

    transform_origin: Point
    """The origin point for rotation and scaling transforms"""

    _qt_object: Optional[QGraphicsItem] = field(init=False, compare=False, repr=False)
    """A corresponding Qt object for internal use only.

    This value is set during rendering and is not meant to be set more than once.
    """

    def render(self):
        """Render the object to the scene.

        This is typically done by constructing a `QGraphicsItem` subclass and calling
        `_register_qt_object` with it. Do *not* manually assign the Qt object's parent
        or add it to the Qt scene.
        """
        raise NotImplementedError

    def _parent_qt_obj(self) -> Optional[QGraphicsItem]:
        if self.parent:
            parent_qt_obj = getattr(self.parent, "_qt_object", None)
            if not parent_qt_obj:
                warn(
                    "Parent interface was provided but corresponding Qt object"
                    + f" not available when needed for {self}"
                )  # implicitly return None
            return parent_qt_obj
        return None

    def _register_qt_object(self, obj: QGraphicsItem):
        parent_obj = self._parent_qt_obj()
        if parent_obj:
            obj.setParentItem(parent_obj)
        else:
            neoscore.app_interface.scene.addItem(obj)
        super().__setattr__("_qt_object", obj)
