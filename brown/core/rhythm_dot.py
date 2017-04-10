from brown.core.music_text import MusicText


class RhythmDot(MusicText):

    """A single rhythmic dot"""

    _glyph_name = 'augmentationDot'

    def __init__(self, pos, parent, font=None):
        """
        Args:
            pos (Point):
            parent (StaffObject):
            font (MusicFont):
        """
        super().__init__(pos, [self._glyph_name], font, parent)
