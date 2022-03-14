from typing import Optional, cast

from neoscore.core.graphic_object import GraphicObject
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.spanner import Spanner
from neoscore.core.staff_object import StaffObject
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import Unit


class RepeatingMusicTextLine(MusicText, StaffObject, Spanner):

    """A spanner of repeating music text over its length."""

    # TODO MEDIUM figure out how to type `text` - same problem as in `MusicText`

    # TODO medium it doesn't really make sense that this supports
    # scale - spanners shouldn't be scaleable since their size is
    # determined by their start/end points.

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
        # Start the MusicText with a single repetition, then after
        # superclasses are set up figure out how many repetitions are
        # needed to cover `self.length` and update the text
        # accordingly.
        MusicText.__init__(self, start, text, parent, font, scale)
        StaffObject.__init__(self, parent)
        Spanner.__init__(self, end_x, end_parent or self)
        self.single_repetition_chars = self.music_chars
        base_width = self.font.bounding_rect_of(self.text).width
        repetitions_needed = int(cast(float, self.length / base_width))
        self.music_chars = self.music_chars * repetitions_needed

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        return self.spanner_x_length
