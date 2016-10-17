#!/usr/bin/env python

from .graphic_object import GraphicObject
from .shared import brown_config
from PySide.QtGui import QGraphicsLineItem, QPen, QBrush, QColor
from .staff_object import StaffObject
from .staff_unit import StaffUnit
from .point_unit import PointUnit


class LedgerLine(StaffObject):
    def __init__(self, parent_column, y_staff_unit_pos):
        """
        Args:
            parent_column (NoteColumn):
            y_staff_unit_pos (StaffUnit or int or float):
        """
        StaffObject.__init__(self, parent_column.parent_staff, parent_column.x_staff_unit_pos, y_staff_unit_pos)

    def build_glyph(self):
        self.glyph = LedgerLineGlyph(self)

    # @property
    # def thickness(self):
    #     """StaffUnit: """
    #     return self._thickness
    #
    # @thickness.setter
    # def thickness(self, new_thickness):
    #     if not isinstance(new_thickness, StaffUnit):
    #         new_thickness = StaffUnit(new_thickness)
    #     self._thickness = new_thickness


class LedgerLineGlyph(QGraphicsLineItem):

    # def __init__(self, parent, scene, x_anchor_pos, y_pos, staff_unit_dist, thickness='default'):
    #     """
    #
    #     Args:
    #         parent:
    #         scene:
    #         x_anchor_pos: The x position of the NoteColumn this presumably is a part of.
    #             Note that this is different from the actual x position which will be passed to the glyph;
    #             the real x position is offset slightly based on staff_height so that the ledger line surrounds
    #             the NoteColumn on either side
    #         y_pos:
    #         staff_unit_dist:
    #         thickness (float or str): Thickness of the line in 72-dpi points
    #
    #     Returns:
    #
    #     """
    #     if thickness == 'default':
    #         thickness = brown_config.default_staff_line_width
    #     if isinstance(parent, GraphicObject):
    #         parent = parent.glyph
    #     # Calculate line length to be 3 staff units
    #     # (3.0 == 9 <number of staff units in a 5-line staff> / 3.0)
    #     line_length = staff_unit_dist * 3
    #     x_start = x_anchor_pos - (line_length / 5.5)  # TODO: Link this more meaningfully to the center of noteheads
    #     # x_start = x_anchor_pos
    #     x_end = x_start + line_length
    #     # TODO: Implement variable thickness ledger lines
    #     QGraphicsLineItem.__init__(self, x_start, y_pos, x_end, y_pos, parent, scene)
    #     self.setPen(QPen(QBrush(QColor(0, 0, 0)), thickness))

    def __init__(self, ledger_line):
        """
        Args:
            ledger_line (LedgerLine):
        """

        # Calculate line length to be 3 staff units
        # (3.0 == 9 <number of staff units in a 5-line staff> / 3.0)
        # These unit conversion are getting very long .......... hmm....
        staff_attributes = ledger_line.staff_attributes
        line_length = staff_attributes.staff_unit_dist.value * 3
        x_start = ledger_line.x_pos.value - (line_length / 5.5)  # TODO: Link this more meaningfully to the center of noteheads
        # x_start = x_anchor_pos
        x_end = x_start + line_length
        y_pos = ledger_line.y_pos.value
        # TODO: Implement variable thickness ledger lines
        QGraphicsLineItem.__init__(self, x_start, y_pos, x_end, y_pos,
                                   ledger_line.parent_staff.glyph, ledger_line.scene)
        # Okay these unit conversions are getting out of hand. Either work in convenience functions
        # or figure out a way to make this simpler
        self.setPen(QPen(QBrush(QColor(0, 0, 0)), staff_attributes.line_width.in_points(staff_attributes).value))

