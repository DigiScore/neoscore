from typing import Optional

from brown.core.graphic_object import GraphicObject
from brown.core.music_font import MusicFont
from brown.core.music_text import MusicText
from brown.core.spanner import Spanner
from brown.core.staff_object import StaffObject
from brown.utils.point import Point, PointDef
from brown.utils.units import Unit


class RepeatingMusicTextLine(MusicText, StaffObject, Spanner):

    """A spanner of repeating music text over its length."""

    # TODO MEDIUM figure out how to type `text` - same problem as in `MusicText`

    def __init__(
        self,
        start: PointDef,
        parent: GraphicObject,
        end_x: Unit,
        text,
        end_parent: Optional[GraphicObject] = None,
        font: Optional[MusicFont] = None,
        scale: float = 1,
    ):
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
            scale (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        start = start if isinstance(start, Point) else Point(*start)
        # init the MusicText to ask it how wide a single
        # repetition of `text` is in order to calculate how many
        # repetitions are needed to cover the spanner.
        MusicText.__init__(self, start, text, parent, font, scale)
        StaffObject.__init__(self, parent)
        Spanner.__init__(self, end_x, end_parent or self)
        self.repeating_music_chars = self.music_chars
        self.repeating_text = self.text
        repetitions = self._repetitions_needed
        self.music_chars = self.music_chars * repetitions
        self._text = self.text * repetitions

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        return self.spanner_x_length

    ######## PRIVATE PROPERTIES ########

    @property
    def _repetitions_needed(self) -> int:
        """int: The number of text repetitions needed to cover the line.

        This value rounds down, such that the real length of the drawn
        text will always be <= self.length.
        """
        base_width = self._char_list_bounding_rect(self.repeating_music_chars).width
        return int(self.length / base_width)
