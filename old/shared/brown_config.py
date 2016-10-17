#!/usr/bin/env python

from ..staff_unit import StaffUnit
from ..point_unit import PointUnit

default_staff_height = PointUnit(17.0)
default_staff_line_width = StaffUnit(0.1)
default_music_font = 'Gonville-11'
default_notehead_padding = StaffUnit(0.35)
# default_stem_thickness = PointUnit(0.5)  # in 72-dpi points
default_stem_thickness = StaffUnit(0.15)  # in 72-dpi points
default_stem_length = StaffUnit(8)  # Length of stems in staff units
default_beam_thickness = StaffUnit(2)
default_color = (0, 0, 0)
