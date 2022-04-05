from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.spanner_2d import Spanner2D
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class RepeatingMusicTextLine(MusicText, Spanner2D):

    """A spanner of repeating music text over its length."""

    # TODO MEDIUM figure out how to type `text` - same problem as in `MusicText`

    def __init__(
        self,
        start: PointDef,
        start_parent: Parent,
        end_pos: PointDef,
        end_parent: Optional[Parent],
        text,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: If no font is given, this or one of its ancestors
                must implement `HasMusicFont`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If `None`, defaults to `self`.
            text (str, tuple, MusicChar, or list of these):
                The text to be repeated over the spanner,
                represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        # Start the MusicText with a single repetition, then after
        # superclasses are set up figure out how many repetitions are
        # needed to cover `self.length` and update the text
        # accordingly.
        MusicText.__init__(self, start, start_parent, text, font)
        Spanner2D.__init__(self, Point.from_def(end_pos), end_parent or self)
        self.rotation = self.angle
        self.single_repetition_chars = self.music_chars
        base_width = self.font.bounding_rect_of(self.text).width
        repetitions_needed = int(cast(float, self.spanner_2d_length / base_width))
        self.music_chars = self.music_chars * repetitions_needed

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_length(self) -> Unit:
        return self.spanner_x_length
