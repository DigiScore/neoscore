from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject


class RhythmDot(MusicText, StaffObject):

    """A single rhythmic dot"""

    _glyph_name = 'augmentationDot'

    def __init__(self, pos, parent, font=None):
        """
        Args:
            pos (Point):
            parent (StaffObject):
            font (MusicFont):
        """
        MusicText.__init__(self, pos, [self._glyph_name], font, parent)
        StaffObject.__init__(self, parent)
