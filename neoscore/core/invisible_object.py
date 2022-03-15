from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.graphic_object import GraphicObject
from neoscore.utils.point import PointDef
from neoscore.utils.units import Unit, ZERO

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class InvisibleObject(GraphicObject):

    """A non-renderable object."""

    def __init__(self, pos: PointDef, parent: Optional[Parent] = None):
        """
        Args:
            pos: The position relative to parent
            parent: The parent object. If None, defaults to the document's first page.
        """
        super().__init__(pos, parent=parent)

    @property
    def length(self) -> Unit:
        return ZERO

    def _render(self):
        """Render all child objects.

        Returns: None
        """
        for child in self.children:
            child._render()

    def _render_before_break(self, *args, **kwargs):
        pass

    def _render_spanning_continuation(self, *args, **kwargs):
        pass

    def _render_after_break(self, *args, **kwargs):
        pass

    def _render_complete(self, *args, **kwargs):
        pass
