from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
# from brown.primitives.chord_rest import ChordRest

"""
Thoughts on the Notehead class

* Does not know what part of a chord it is in (is not aware of its context)
* Does have an accidental


"""

class Notehead(StaffObject):

    def __init__(self, parent_staff, position, pitch):
        """
        Args:
            parent_staff (Staff):
            position (float):
            pitch (Pitch):
        """
        self.parent_staff = parent_staff
        self.position = position
        self.pitch = pitch
        self.grob = Glyph(
            parent_staff.x + position,
            0,
            '\uE13E', Font('gonville', 20))

    def render(self):
        self.grob.render()
