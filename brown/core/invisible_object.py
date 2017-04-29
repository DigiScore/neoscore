from brown.core.graphic_object import GraphicObject


class InvisibleObject(GraphicObject):

    """A non-renderable object."""

    _interface_class = None

    def __init__(self, pos, parent=None):
        """
        Args:
            pos (Point or init tuple): The position of the path root
                relative to the document.
            parent: The parent object or None
        """
        super().__init__(pos, parent=parent)

    def render(self):
        """Render all child objects.

        Returns: None
        """
        for child in self.children:
            child.render()
