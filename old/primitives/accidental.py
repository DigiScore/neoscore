#!/usr/bin/env python

from .staff_object import StaffObject
from .staff_unit import StaffUnit
from .point_unit import PointUnit
from .tools.staff_tools import y_of_staff_pos
from .music_string_glyph import MusicStringGlyph
from .music_font import MusicFont


class AccidentalObject(StaffObject):
    """
    A StaffObject accidental.

    This object inherits nearly all of its attributes from a parent Notehead object, including
    what type of accidental it actually is.
    """
    def __init__(self, parent_notehead, x_staff_unit_offset=0):
        """
        Args:
            parent_notehead (Notehead):
            x_staff_unit_offset (StaffUnit or float or int):
        """
        if not isinstance(x_staff_unit_offset, StaffUnit):
            x_staff_unit_offset = StaffUnit(x_staff_unit_offset)
        x_staff_unit_pos = parent_notehead.x_staff_unit_pos + x_staff_unit_offset
        StaffObject.__init__(self, parent_notehead.parent_staff,
                             x_staff_unit_pos, parent_notehead.y_staff_unit_pos)
        self.parent_notehead = parent_notehead

    def build_glyph(self):
        self.glyph = AccidentalGlyph(self)


class AccidentalGlyph(MusicStringGlyph):

    def __init__(self, accidental_object):
        """
        Args:
            accidental_object (AccidentalObject):
        """
        # TODO: allow accidentals to be more elegantly flushed left based on the bounding box of the glyph
        # TODO: move this transformation element to the Accidental container?
        # For legibility, store a few local variables
        staff = accidental_object.parent_staff
        accidental = accidental_object.parent_notehead.named_pitch.accidental
        staff_unit_dist = accidental_object.staff_attributes.staff_unit_dist.value
        offset_dict = {'double flat': -0.25, 'flat': 0.25, 'natural': -0.15,
                       'sharp': -0.25, 'double sharp': -0.25}
        glyph_string = accidental.unicode_value
        # x_pos = x_anchor_pos + (offset_dict[accidental.name] * staff.staff_unit_dist)
        x_pos = PointUnit(accidental_object.x_pos.value + (staff_unit_dist * offset_dict[accidental.name]))

        # This use of scale=staff_height/17.0 assumes 17.0 is the default, may need to be tweaked
        MusicStringGlyph.__init__(self, accidental_object.parent_staff.glyph, accidental_object.scene, glyph_string,
                                  x_pos, accidental_object.y_pos, MusicFont('Gonville'),
                                  accidental_object.staff_attributes,
                                  scale=accidental_object.staff_attributes.height.value / 17.0)
