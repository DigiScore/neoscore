#!/usr/bin/env python

from .music_string_glyph import MusicStringGlyph
from .rhythmic_value import RhythmicValue
from PySide.QtGui import QTransform
from .music_font import MusicFont
from .staff_object import StaffObject
from .staff_unit import StaffUnit
from .point_unit import PointUnit


class Flag(StaffObject):
    """
    A flag to be used in conjunction with stems in a NoteColumn.

    Inherits nearly all of its data from its parent NoteColumn
    """
    def __init__(self, parent_column, y_staff_unit_pos):
        """
        Args:
            parent_column (NoteColumn):
            y_staff_unit_pos (StaffUnit or int or float):
        """
        x_staff_unit_pos = parent_column.x_staff_unit_pos + StaffUnit(0.25)
        StaffObject.__init__(self, parent_column.parent_staff, x_staff_unit_pos, y_staff_unit_pos)
        self.parent_column = parent_column
        self.direction = self.parent_column.stem_direction
        if self.direction == 1:
            self.x_staff_unit_pos += self.staff_attributes.approx_notehead_width

    @property
    def parent_column(self):
        """NoteColumn: The NoteColumn this Flag belongs to"""
        return self._parent_column

    @parent_column.setter
    def parent_column(self, new_parent_column):
        if not type(new_parent_column).__name__ == 'NoteColumn':
            raise TypeError('Flag.parent_column must be of type NoteColumn')
        self._parent_column = new_parent_column

    @property
    def direction(self):
        """int: The direction the flag points. 1 means point up, -1 means point down"""
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if not (new_direction == 1 or new_direction == -1):
            raise ValueError('Flag.direction must be -1 or 1')
        self._direction = new_direction

    def build_glyph(self):
        self.glyph = FlagGlyph(self)
        return self.glyph


class FlagGlyph(MusicStringGlyph):
    """
    A glyph containing rhythm stem flags
    """

    def __init__(self, flag):
        """
        Args:
            flag (Flag):
        """
        glyph_dict = {8: '\uE180', 16: '\uE182', 32: '\uE184', 64: '\uE186', 128: '\uE188'}
        glyph_string = glyph_dict[flag.parent_column.duration.base_value]
        staff_height = flag.staff_attributes.height
        MusicStringGlyph.__init__(self, flag.parent_staff.glyph, flag.scene, glyph_string, flag.x_pos, flag.y_pos,
                                  MusicFont('Gonville'), flag.staff_attributes, scale=staff_height.value / 17.0)
        if flag.direction == 1:
            # Music font glyphs already point up, no transform needed
            pass
        elif flag.direction == -1:
            # Flip if facing down
            self.setTransform(QTransform.fromScale(1, -1))
        else:
            raise ValueError