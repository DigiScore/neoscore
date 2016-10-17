#!/usr/bin/env python

from .music_string_glyph import MusicFont, MusicStringGlyph
from .staff_object import StaffObject
from .staff_unit import StaffUnit


class RhythmDot(StaffObject):
    """
    A rhythm dot
    """
    def __init__(self, parent_notehead, x_staff_unit_offset):
        """
        Args:
            parent_notehead (Notehead or Rest):
            x_staff_unit_offset (StaffUnit or float or itn):
            scale (float or int): Factor by which the rhythm dot will be scaled
        """
        if not isinstance(x_staff_unit_offset, StaffUnit):
            x_staff_unit_offset = StaffUnit(x_staff_unit_offset)
        x_staff_unit_pos = parent_notehead.x_staff_unit_pos + x_staff_unit_offset
        StaffObject.__init__(self, parent_notehead.parent_staff, x_staff_unit_pos, parent_notehead.y_staff_unit_pos)

        # self.glyph = RhythmDotGlyph(self)
        self.build_glyph()

    def build_glyph(self):
        self.glyph = RhythmDotGlyph(self)
        return self.glyph


class RhythmDotGlyph(MusicStringGlyph):

    def __init__(self, rhythm_dot):
        """
        Args:
            rhythm_dot (RhythmDot):
        """
        staff_height = rhythm_dot.staff_attributes.height
        MusicStringGlyph.__init__(self, rhythm_dot.parent_staff.glyph, rhythm_dot.parent_staff.scene,
                                  '\uE17C', rhythm_dot.x_pos, rhythm_dot.y_pos, MusicFont('Gonville'),
                                  rhythm_dot.staff_attributes, staff_height.value / 17.0 / 1.5)
