from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.utils.point import PointDef
from neoscore.utils.units import Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class RepeatingMusicTextLine(MusicText, Spanner):

    """A spanner of repeating music text over its length."""

    # TODO MEDIUM figure out how to type `text` - same problem as in `MusicText`

    # TODO MEDIUM maybe reorder args here so end_x and end_parent are
    # adjacent. see how other spanners do this.

    def __init__(
        self,
        start: PointDef,
        start_parent: Parent,
        end_x: Unit,
        text,
        end_parent: Optional[PositionedObject] = None,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: If no font is given, this or one of its ancestors
                must implement `HasMusicFont`.
            end_x: The end x position.
            text (str, tuple, MusicChar, or list of these):
                The text to be repeated over the spanner,
                represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            end_parent: An optional parent of the end point.
                If omitted, the end position is relative to the main object.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        # Start the MusicText with a single repetition, then after
        # superclasses are set up figure out how many repetitions are
        # needed to cover `self.length` and update the text
        # accordingly.
        MusicText.__init__(self, start, start_parent, text, font)
        Spanner.__init__(self, end_x, end_parent or self)
        self.single_repetition_chars = self.music_chars
        base_width = self.font.bounding_rect_of(self.text).width
        repetitions_needed = int(cast(float, self.length / base_width))
        self.music_chars = self.music_chars * repetitions_needed

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        return self.spanner_x_length
