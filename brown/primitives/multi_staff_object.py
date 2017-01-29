class MultiStaffObject:

    """An object which spans several staves.

    This is a Mixin class, meant to be combined with GraphicObject classes.
    This Mixin class is incompatible with StaffObject.
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
