from brown.utils.units import StaffUnit
from brown.utils.point import Point


class StaffPoint(Point):

    """A point in a staff.

    Unlike a typical point, a `StaffPoint` must be attached to a staff,
    and its y value represents a position in staff spaces relative to
    the staff. A staff position of 0 represents the center line of the staff
    while higher values move upward and lower values move downward.

    Like a `Point` a `StaffPoint`'s x and y values may be accessed
    by name, iteration, and indexing:

        >>> p = StaffPoint(Mm(5), 1)  # Would be C5 in treble clef
        >>> p.x == p[0] == 5
        True
        >>> p.y == p[1] == 6
        True
        >>> x, y = p
        >>> x
        5
        >>> y
        6
    """
    def __init__(self, pos, staff):
        """
        # NOTE: This uses a much more restricted call signature than has been
        #       the case with earlier Point classes. Probably it's better to
        #       move more toward this practice to keep the API simple.

        Args:
            pos (Point or 2-tuple(Unit, float)): The staff position of
                the point. The x axis should be a Unit while the y-axis
                may be either a simple number or a `StaffUnit`.
                If it is a `StaffUnit`, its `staff` must be the same as
                the `staff` argument.
            staff (Staff): The staff this point belongs in
        """
        self._x = pos[0]
        if isinstance(pos[1], StaffUnit):
            if pos[1].staff != staff:
                raise ValueError(
                    'staff in `pos`, if present, must be the same as `staff`')
            self._y = pos[1]
        else:
            self._y = StaffUnit(pos[1], staff)

        self._iter_index = 0

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return '{}(({}, {}), {})'.format(
            type(self).__name__, self.x, self.y, self.staff)

    ######## PRIVATE CLASS METHODS ########

    @classmethod
    def with_unit(cls, pos, staff, unit):
        """Create a Point and ensure its coordinates are in a type of unit.

        Args:
            pos (Point or 2-tuple(Unit, float)): The staff position of
                the point. The x axis should be a Unit while the y-axis
                may be either a simple number or a `StaffUnit`.
                If it is a `StaffUnit`, its `staff` must be the same as
                the `staff` argument.
            staff (Staff): The staff this point belongs in
            unit (type): A `Unit` class
        """
        point = cls(pos, staff)
        point.to_unit(unit)
        return point

    ######## PUBLIC METHODS ########

    def to_unit(self, unit):
        """Translate the x value to be in a certain type.

        Because this is a StaffPoint the y axis *must* be a `StaffUnit`
        and this method has no effect on `self.y`

        Args:
            unit (type): A Unit class.

        Returns: None
        """
        self.x = unit(self.x)
