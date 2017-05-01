from brown.utils.exceptions import NoAncestorStaffError
from brown.core.graphic_object import GraphicObject


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with GraphicObject classes.

    Usage within a GraphicObject will look something like:

        class SomeStaffGlyphObject(MusicText, StaffObject):
            def __init__(self, pos, parent):
                MusicText.__init__(self, 'someGlyphName', parent)
                StaffObject.__init__(self, parent)
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

    @property
    def pos_in_staff(self):
        """Point: The position of this object relative to the staff.

        This position is in non-flowed space.

        # TODO: Definitely cache me when property caching is implemented
        """
        if self.frame:
            return self.frame.map_between_items_in_frame(self.staff, self)
        return GraphicObject.map_between_items(self.staff, self)

    ######## PRIVATE METHODS ########

    @staticmethod
    def find_staff(graphic_object):
        """Find the first staff which is `graphic_object` or an ancestor of it.

        Args:
            graphic_object (GraphicObject):

        Returns: Staff or None
        """
        if type(graphic_object).__name__ == 'Staff':
            return graphic_object
        return graphic_object.first_ancestor_of_exact_class('Staff')
