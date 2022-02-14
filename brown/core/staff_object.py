from brown.core.graphic_object import GraphicObject
from brown.utils.exceptions import NoAncestorStaffError


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with GraphicObject classes.

    Usage within a GraphicObject will look something like:

    >>> class SomeMusicGlyph(MusicText, StaffObject):  # doctest: +SKIP
    ...     def __init__(self, ...):
    ...         MusicText.__init__(self, ...)
    ...         StaffObject.__init__(self, ...)
    """

    def __init__(self, parent):
        """
        Args:
            parent (Staff or StaffObject):
        """
        self._staff = self.find_staff(parent)
        if not self._staff:
            raise NoAncestorStaffError

    ######## PUBLIC PROPERTIES ########

    @property
    def staff(self):
        """Staff: The staff associated with this object"""
        return self._staff

    # TODO this is very slow. one simple optimization would be
    # specializing the subroutines to compute X positions only, since
    # they're all that's needed for this. it would be noisy, but it
    # could improve speed by nearly half. Alternatively this could be
    # cached, but invalidation is tricky.
    @property
    def pos_in_staff(self):
        """Point: The position of this object relative to the staff.

        This position is in non-flowed space.
        """
        if self.flowable:
            return self.flowable.map_between_locally(self.staff, self)
        return GraphicObject.map_between_items(self.staff, self)

    ######## PRIVATE METHODS ########

    @staticmethod
    def find_staff(graphic_object):
        """Find the first staff which is `graphic_object` or an ancestor of it.

        Args:
            graphic_object (GraphicObject):

        Returns: Staff or None
        """
        if type(graphic_object).__name__ == "Staff":
            return graphic_object
        return graphic_object.first_ancestor_of_exact_class("Staff")
