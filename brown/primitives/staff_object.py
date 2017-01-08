class NoAncestorStaffError(Exception):
    """Exception raised when a StaffObject does not have an ancestor Staff"""
    pass


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with GraphicObject classes.

    Usage within a GraphicObject will look something like:

        class SomeStaffGlyphObject(MusicGlyph, StaffObject):
            def __init__(self, pos, parent):
                MusicGlyph.__init__(self, 'someGlyphName', parent)
                StaffObject.__init__(self, parent)
    """

    def __init__(self, parent):
        self._staff = self._find_staff(parent)
        if not self._staff:
            raise NoAncestorStaffError
        self.staff._register_staff_object(self)  # Register object with staff

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
