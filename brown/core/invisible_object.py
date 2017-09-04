from brown.core.graphic_object import GraphicObject


class InvisibleObject(GraphicObject):

    """A non-renderable object."""

    def __init__(self, pos, parent=None):
        """
        Args:
            pos (Point or init tuple): The position of the path root
                relative to the document.
            parent: The parent object or None
        """
        super().__init__(pos, parent=parent)

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
