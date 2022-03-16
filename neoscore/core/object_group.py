from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


# TODO MEDIUM maybe this class should be removed since it doesn't
# really do anything PositionedObject can't already.


class ObjectGroup(PositionedObject):

    """A collection of `PositionedObject`s."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent] = None,
        objects: Optional[set[PositionedObject]] = None,
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
