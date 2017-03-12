from brown.core.graphic_object import GraphicObject


class MultiStaffObject:

    """An object which spans several staves.

    This is a Mixin class, meant to be combined with GraphicObject classes.

    If an class is both a MultiStaffObject and a StaffObject, the parent staff
    should be the top staff listed in `self.staves`.

    MultiStaffObjects will typically have their visually highest staff
    as their parent.

    In most MultiStaffObject classes, object-wide property will be derived
    from the visually highest staff.

    TODO: Cache potentially expensive property calculations
    """

    def __init__(self, staves):
        """
        Args:
            staves(set{Staff}): The set of Staff objects this belongs to.
        """
        self.staves = staves


    ######## PUBLIC PROPERTIES ########

    @property
    def visually_sorted_staves(self):
        """list[Staff]: self.staves as a list in visually descending order"""
        return sorted(list(self.staves),
                      key=lambda s: s.y)

    @property
    def highest_staff(self):
        """Staff: The visually highest staff in self.staves"""
        return self.visually_sorted_staves[0]

    @property
    def lowest_staff(self):
        """Staff: The visually lowest staff in self.staves"""
        return self.visually_sorted_staves[-1]

    @property
    def vertical_span(self):
        """StaffUnit: The vertical distance covered by the staves

        The distance from the top of `self.highest_staff` to the bottom
        of `self.lowest_staff`, in `self.highest_staff.unit` StaffUnits.
        """
        return self.highest_staff.unit(GraphicObject.map_between_items(
                                           self.highest_staff,
                                           self.lowest_staff).y
                                       + self.lowest_staff.height)