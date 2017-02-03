from brown.core.graphic_object import GraphicObject
from brown.core.music_text_object import MusicTextObject
from brown.core.recurring_object import RecurringObject
from brown.primitives.multi_staff_object import MultiStaffObject


class Brace(RecurringObject, MultiStaffObject, MusicTextObject):

    def __init__(self, pos_x, length, staves):
        """
        Args:
            pos_x (Unit): Where this brace goes into effect
            length (Unit): How long this brace is in effect
            staves (set{Staff}): The staves this brace spans
        """
        MultiStaffObject.__init__(self, staves)
        # Calculate the height of the brace in highest_staff staff units
        height = (GraphicObject.map_between_items(self.highest_staff,
                                                  self.lowest_staff).y
                  + self.lowest_staff.height)
        scale = height / self.highest_staff.unit(4)
        MusicTextObject.__init__(self,
                                 (pos_x, height),
                                 ['brace'],
                                 self.highest_staff,
                                 scale_factor=scale)
        self._breakable_width = length
        # Recur at line start
        RecurringObject.__init__(self, 0)

    def _render_occurence(self, pos):
        self._render_complete(pos)
