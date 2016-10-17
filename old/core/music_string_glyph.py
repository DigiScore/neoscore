#!/usr/bin/env python

from PySide.QtGui import QGraphicsItem, QFont, QPen, QBrush, QColor
from PySide.QtCore import QRectF
from .shared import brown_config
from .music_font import MusicFont


class MusicStringGlyph(QGraphicsItem):
    """
    A subclass of QGraphicsItem which draws a string of text.

    """
    def __init__(self, parent, scene, string, x_pos, y_pos, music_font, staff_attribute_set, scale=1.0):
        """

        Args:
            parent (QGraphicsItem):
            scene (QGraphicsItem):
            string (str):
            x_pos (PointUnit):
            y_pos (PointUnit):
            music_font (MusicFont or str):
            staff_attribute_set (StaffAttributeSet):
            scale (float):
        """
        QGraphicsItem.__init__(self, parent=parent, scene=scene)
        self.setPos(x_pos.value, y_pos.value)
        self.staff_attribute_set = staff_attribute_set
        self.scale = scale
        self.string = string
        self.music_font = music_font
        self._font_size_multiplier = 14  # An internal-use constant. May need to be tweaked (or better, removed)

    @property
    def music_font(self):
        return self._music_font
    
    @music_font.setter
    def music_font(self, new_music_font):
        if isinstance(new_music_font, str):
            new_music_font = MusicFont(new_music_font)
        elif not isinstance(new_music_font, MusicFont):
            raise TypeError('StringGlyph.music_font must be a MusicFont')
        self._music_font = new_music_font
    
    def paint(self, painter, option, widget):
        # Set font to self.font. Use self.scale and self._font_size_multiplier for the font size
        painter.setFont(QFont(self.music_font.registered_font_name, self.scale * self._font_size_multiplier))
        painter.setPen(QPen(QBrush(QColor(*brown_config.default_color)), 0))
        x_pos = self.staff_attribute_set.staff_unit_dist.value * self.music_font.x_offset
        y_pos = self.staff_attribute_set.staff_unit_dist.value * self.music_font.y_offset * -1

        painter.drawText(x_pos, y_pos, self.string)

    def boundingRect(self):
        # TODO: Calculate from bounding box of str?
        return QRectF(0, 0, 30, 30)
