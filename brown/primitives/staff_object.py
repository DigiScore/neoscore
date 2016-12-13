from brown.utils.units import GraphicUnit, Mm, StaffUnit
from brown.utils.point import Point
from brown.core.graphic_object import GraphicObject
# from brown.primitives.staff import Staff


class StaffObject(GraphicObject):

    """An object which is the *immediate* child of a Staff

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
        # if not isinstance(parent, Staff):
        #     raise TypeError('StaffObject parent must be a Staff')
        self._parent = parent
        self.staff._register_staff_object(self)  # Register object with staff

    ######## PUBLIC PROPERTIES ########

    @property
    def staff(self):
        """The staff associated with this object"""
        # TODO: Remove me once this code moves forward more
        return self.parent
