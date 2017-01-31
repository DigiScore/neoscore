from brown.core.graphic_object import GraphicObject
from brown.core.music_glyph import MusicGlyph
from brown.primitives.multi_staff_object import MultiStaffObject


class Brace(MultiStaffObject, MusicGlyph):

    def __init__(self, pos_x, staves):
        """
        Args:
            pos_x(Unit): Where this brace goes into effect
            staves(set{Staff}): The staves this brace spans
        """
        MultiStaffObject.__init__(self, staves)
        # Calculate the height of the brace in highest_staff staff units
        height = (GraphicObject.map_between_items(self.highest_staff,
                                                  self.lowest_staff).y
                  + self.lowest_staff.height)
        scale = height / self.highest_staff.unit(4)
        MusicGlyph.__init__(self,
                            (pos_x, height),
                            'brace',
                            parent=self.highest_staff,
                            scale_factor=scale)
