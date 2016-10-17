#!/usr/bin/env python
from .staff_object import StaffObject
from .music_string_glyph import MusicStringGlyph
from .shared import brown_config
from .tools.staff_tools import y_of_staff_pos
from .shared import brown_config
from .music_font import MusicFont


class Clef(StaffObject):
    """
    Clef object containing a Glyph reference and a pitch_position
    """
    def __init__(self, parent_staff, clef_type, x_staff_unit_pos):
        """
        Args:
            parent_staff (Staff):
            clef_type (str):
            x_staff_unit_pos (float):
        """
        StaffObject.__init__(self, parent_staff, x_staff_unit_pos, 0)
        if clef_type not in ['treble 8va', 'treble', 'treble 8vb', 'tenor', 'alto', 'bass', 'bass 8vb']:
            raise ValueError('clef_name of %s is invalid' % clef_type)
        self._clef_name = clef_type
        # TODO: implement 8va and 8vb clefs (maybe as a compound StringGlyph somehow?)
        if clef_type == 'treble':
            self._pitch_position = 11
            self.y_staff_unit_pos = -2
            self.glyph_string = '\uE118'
        elif clef_type == 'bass':
            self._pitch_position = -10
            self.y_staff_unit_pos = 2
            self.glyph_string = '\uE117'
        elif clef_type == 'treble 8va':
            self._pitch_position = 23
            self.y_staff_unit_pos = -2
            self.glyph_string = '\uE118'
        elif clef_type == 'treble 8vb':
            self._pitch_position = -1
            self.y_staff_unit_pos = -2
            self.glyph_string = '\uE118'
        elif clef_type == 'tenor':
            self.y_staff_unit_pos = 2
            self._pitch_position = -3
            self.glyph_string = '\uE116'
        elif clef_type == 'alto':
            self.y_staff_unit_pos = 0
            self._pitch_position = 0
            self.glyph_string = '\uE116'
        elif clef_type == 'bass 8vb':
            self.y_staff_unit_pos = 2
            self._pitch_position = -22
            self.glyph_string = '\uE116'
        else:
            raise ValueError('clef_name of %s is invalid' % clef_type)

        self.build_glyph()

    @property
    def clef_name(self):
        return self._clef_name

    @property
    def pitch_position(self):
        """int: A reference indicating how pitches correspond to staff spaces in this clef:
        the number indicates the pitch number which corresponds to the center line in this clef
        if a natural-accidental note were placed there. e.g. ``11`` indicates treble clef,
        because the center line relates to B"""
        return self._pitch_position

    def build_glyph(self):
        self.glyph = MusicStringGlyph(self.parent_staff.glyph, self.parent_staff.scene, self.glyph_string,
                                      self.x_pos, self.y_pos,
                                      MusicFont('Gonville'), self.staff_attributes,
                                      self.staff_attributes.height / 17.0)
