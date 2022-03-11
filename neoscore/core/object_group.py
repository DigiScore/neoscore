from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.graphic_object import GraphicObject
from neoscore.core.invisible_object import InvisibleObject
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class ObjectGroup(InvisibleObject):

    """An abstract collection of GraphicObjects."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent] = None,
        objects: Optional[set[GraphicObject]] = None,
    ):
        """
        Args:
            pos: The local position
            parent: The object's parent
            objects: The objects in the group.
        """
        super().__init__(pos, parent=parent)
        if objects:
            for child in objects:
                self._register_child(child)
