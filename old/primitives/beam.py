#!/usr/bin/env python

from PySide.QtGui import QColor, QGraphicsPathItem, QPainterPath

from .shared import brown_config
from .tools import staff_tools, unit_tools


class Beam:
    """
    A data container for beams.
    """
    def __init__(self, parent_staff, x_start, x_stop, y_staff_pos_start, y_staff_pos_stop, thickness='default'):
        """
        
        Args:
            parent_staff (Staff): 
            x_start (float): x-axis starting position in 72-dpi units
            x_stop (float): x-axis ending position in 72-dpi units
            y_staff_pos_start (float or int): vertical starting staff position
            y_staff_pos_stop (float or int): vertical ending staff position
            thickness (float): thickness of this Beam in  staff units

        Returns:

        """
        # TODO: Handle multiple beams and beamlets
        self.parent_staff = parent_staff
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_staff_pos_start = y_staff_pos_start
        self.y_staff_pos_stop = y_staff_pos_stop
        self.y_start = staff_tools.y_of_staff_pos(self.parent_staff.attributes_at(self.x_start), self.y_staff_pos_start)
        self.y_stop = staff_tools.y_of_staff_pos(self.parent_staff.attributes_at(self.x_start), self.y_staff_pos_stop)
        if self.thickness == 'default':
            self.thickness = brown_config.default_beam_thickness
        else:
            self.thickness = thickness

    @property
    def slope(self):
        """float: The slope of the beam in 72-dpi points. Note that a positive slope
        indicates a beam which moves down from left to right"""
        # Multiply delta x by 1.0 to prevent possible rounding errors if values are int
        return (self.y_stop - self.y_start) / ((self.x_stop - self.x_start) * 1.0)

    def build_glyph(self):
        """
        Build and return a BeamGlyph object
        Returns: BeamGlyph
        """
        # Experimental alternative implementation
        return BeamGlyph(self)


class BeamGlyph(QGraphicsPathItem):

    def __init__(self, beam):
        """

        Args:
            beam (Beam): The Beam object from which to initialize

        """
        self.x_start = beam.x_start
        self.x_stop = beam.x_stop
        self.y_start = beam.y_start
        self.y_stop = beam.y_stop
        if beam.thickness == 'default':
            self.thickness = brown_config.default_beam_thickness
        else:
            self.thickness = beam.thickness
        QGraphicsPathItem.__init__(self, beam.parent_staff.glyph, beam.parent_staff.scene)
        self.setPath(self.build_path())
        self.setBrush(QColor(0, 0, 0))

    def build_path(self):
        """
        Builds a QPainterPath object based on the contents of this BeamGlyph and returns it

        Returns: QPainterPath

        """
        path = QPainterPath()
        path.moveTo(self.x_start, self.y_start)
        path.lineTo(self.x_start, self.y_start - self.thickness)
        path.lineTo(self.x_stop, self.y_stop - self.thickness)
        path.lineTo(self.x_stop, self.y_stop)
        path.closeSubpath()
        return path
