from brown.core.horizontal_spanner import HorizontalSpanner
from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.utils.point import Point


class RepeatingMusicTextLine(MusicText, StaffObject, HorizontalSpanner):

    """A spanner of repeating music text over its length."""

    def __init__(self, start, parent, end_x, text, end_parent=None,
                 font=None, scale_factor=1):
        """
        Args:
            start (Point or init tuple): The starting point.
            parent (GraphicObject): The parent of the starting point.
            end_x (Unit): The end x position.
            text (str, tuple, MusicChar, or list of these):
                The text to be repeated over the spanner,
                represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            end_parent (GraphicObject): An optional parent of the end point.
                If omitted, the end position is relative to the main object.
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        start = start if isinstance(start, Point) else Point(*start)
        # init the MusicText to ask it how wide a single
        # repetition of `text` is in order to calculate how many
        # repetitions are needed to cover the spanner.
        MusicText.__init__(self, start, text, parent, font, scale_factor)
        StaffObject.__init__(self, parent)
        HorizontalSpanner.__init__(self, end_x, end_parent)
        self.repeating_music_chars = self.music_chars
        self.repeating_text = self.text
        repetitions = self._repetitions_needed
        self.music_chars = self.music_chars * repetitions
        self._text = self.text * repetitions

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        return self.spanner_x_length

    ######## PRIVATE PROPERTIES ########

    @property
    def _repetitions_needed(self):
        """int: The number of text repetitions needed to cover the line.

        This value rounds down, such that the real length of the drawn
        text will always be <= self.length.
        """
        base_width = self._char_list_bounding_rect(
            self.repeating_music_chars).width
        return int((self.length / base_width).value)
