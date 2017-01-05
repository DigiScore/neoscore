from brown.core.invisible_object import InvisibleObject


class ObjectGroupLookupError(Exception):
    """Error raised when trying to access a nonexistent ObjectGroup member"""
    pass


class ObjectGroup(InvisibleObject):

    # TODO: The implementation here is pretty hacky,
    #       revisit when this needs to be more robust

    def __init__(self, pos, parent=None, objects=None):
        """
        Args:
            pos (Point[Unit] or tuple): The local position
            parent (GraphicObject or None): The object's parent
            objects (set{GraphicObject}): The objects in the group.
        """
        super().__init__(pos, parent=parent)
        self._objects = objects if objects else set()

    ######## PUBLIC PROPERTIES ########

    @property
    def objects(self):
        """set{GraphicObject}: The objects in the group."""
        return self._objects

    ######## PUBLIC METHODS ########

    def register_object(self, graphic_object):
        """Register an object in this group.

        If the object already exists in the group, this does nothing.

        Args:
            graphic_object (GraphicObject): The item to be added

        Returns: None
        """
        self.objects.add(graphic_object)

    def remove_object(self, graphic_object):
        """Remove an object from the group.

        If the object does not exist in the group,
        this raises an ObjectGroupLookupError.

        Args:
            graphic_object (GraphicObject): The item to be removed

        Returns: None
        """
        try:
            self.objects.remove(graphic_object)
        except KeyError:
            raise ObjectGroupLookupError(
                'Object "{}" not found in group'.format(graphic_object))

    def render(self):
        """Renders the entire object group to the scene.

        Returns: None
        """
        super().render()
        for item in self.objects:
            item.render()
