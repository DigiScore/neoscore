from brown.utils.point import Point
from brown.utils.units import Unit


class NoAncestorStaffError(Exception):
    """Exception raised when a StaffObject does not have an ancestor Staff"""
    pass


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with GraphicObject classes.

    Usage within a GraphicObject will look something like:

        class SomeStaffGlyphObject(MusicTextObject, StaffObject):
            def __init__(self, pos, parent):
                MusicTextObject.__init__(self, ['someGlyphName'], parent)
                StaffObject.__init__(self, parent)
    """

    def __init__(self, parent):
        """
        Args:
            parent (Staff or StaffObject):
        """
        self._staff = self._find_staff(parent)
        if not self._staff:
            raise NoAncestorStaffError

    ######## PUBLIC PROPERTIES ########

    @property
    def staff(self):
        """Staff: The staff associated with this object"""
        return self._staff

    ######## PRIVATE METHODS ########

    @staticmethod
    def _find_staff(graphic_object):
        """Find the first staff which is `graphic_object` or an ancestor of it.

        Returns: Staff or None
        """
        current = graphic_object
        while True:
            # NOTE: This has the potential to fall into an infinite loop
            #       if cyclic parentage exists. This should be protected
            #       against in higher-up GraphicObject parent setters
            if current is None or (not hasattr(current, 'parent')):
                return None
            elif type(current).__name__ == 'Staff':
                return current
            else:
                current = current.parent

    ######## PUBLIC METHODS ########

    def map_to_staff_unflowed(self):
        """Map to the position in the unflowed staff.

        Unflowed meaning the position along the total staff length
        without line- or page-breaks.
        """
        delta = Point(type(self.x)(0), type(self.y)(0))
        current = self
        while current != self.staff:
            delta += current.pos
            current = current.parent
        return delta
