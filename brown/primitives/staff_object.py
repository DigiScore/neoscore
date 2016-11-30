from brown.utils.units import GraphicUnit, Mm, StaffUnit
from brown.utils.point import Point
from brown.utils.staff_point import StaffPoint


class NoAncestorStaffError(Exception):
    """Exception raised when no ancestor of a StaffObject is a Staff."""
    pass


class StaffObject(GraphicUnit):

    """An object in a staff

    Note that coordinates in a StaffObject are different than in a
    typical GraphicObject. While the x-axis still refers to typical
    units relative to the staff origin, the y-axis should be an *integer*
    representing the position in staff units relative to the center staff line.
    Positive values indicate higher pitches and visually higher locations
    while negative values indicate the reverse.

    For example, in a 5-line staff `staff_pos=Point(Mm(30), 1)` would indicate 30 mm
    horizontally past the staff origin and the first above the center
    (C5 in treble clef).
    """

    def __init__(self, staff_pos, breakable_width, parent):
        """
        Args:
            TODO: Docs!
        """
        temp_pos = (0, 0)  # HACK: Set a temp position, fix me later
        super().__init__(pos=temp_pos,
                         breakable_width=breakable_width,
                         parent=parent)
        self._parent = parent
        self.staff._register_staff_object(self)
        self.pos = self.staff._staff_pos_to_rel_pixels(staff_pos.y)

    ######## PUBLIC PROPERTIES ########

    @property
    def staff_pos(self):
        """StaffPoint: The position of the object relative to its parent."""
        return self._pos

    @staff_pos.setter
    def staff_pos(self, value):
        self._staff_pos = Point.with_unit(value, unit=GraphicUnit)
        if self._interface:
            self._interface.pos = self._pos

    @property
    def pos(self):
        """Point: The position of the object relative to its parent."""
        if self.staff == self.parent:
            return Point(self.staff_pos.x,
                         self.staff._staff_pos_to_rel_pixels(
                             self.staff_pos.y))
        return self._pos  # TODO: Implement more functions (in Staff?)
        # breaking apart the translation of staff
        # space to flowable space.

    @pos.setter
    def pos(self, value):
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        if self._interface:
            self._interface.pos = self._pos

    @property
    def staff(self):
        """The staff associated with this object"""
        try:
            ancestor = self.parent
            while type(ancestor).__name__ != 'Staff':
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            raise NoAncestorStaffError

    @property
    def position_y_in_staff_units(self):
        """float: The y position in staff units below top of the staff.

        0 means exactly at the top staff line.
        Positive values extend *downward* below the top staff line
        while negative values extend *upward* above the top staff line.
        """
        raise NotImplementedError

    @position_y_in_staff_units.setter
    def position_y_in_staff_units(self, value):
        raise NotImplementedError
