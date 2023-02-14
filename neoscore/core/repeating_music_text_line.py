from __future__ import annotations

from typing import Optional, cast

from neoscore.core.brush import BrushDef
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicStringDef, MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.units import ZERO, Unit


class RepeatingMusicTextLine(Spanner2D, MusicText):

    """A spanner of repeating music text over its length.

    This automatically rotates the text to support 2D lines, but
    please note that rotated text breaking across flowable lines is
    not yet fully supported and will display incorrectly.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: Optional[PositionedObject],
        end_pos: PointDef,
        end_parent: Optional[PositionedObject],
        text: MusicStringDef,
        start_cap_text: Optional[MusicStringDef] = None,
        end_cap_text: Optional[MusicStringDef] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        background_brush: Optional[BrushDef] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: If no font is given, this or one of its ancestors
                must implement :obj:`.HasMusicFont`.
            end_pos: The end point.
            end_parent: The parent for the ending position.
                If ``None``, defaults to ``self``. (Note the lack of a default
                argument here: unlike with most other spanners, ``None`` must be given
                explicitly.)
            text: The text to be repeated over the spanner. Can be given as a SMuFL
                glyph name, or other shorthand forms. See :obj:`.MusicStringDef`.
            start_cap_text: A text specifier for the start of the text. Useful for
                things like "tr" beginnings to trill lines. This can be provided in the
                same form as ``text``.
            end_cap_text: A text specifier for the end of the text. Especially useful
                for line terminators like arrows at the end of arppeggio lines.
                This can be provided in the same form as ``text``.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
        """
        # Start the MusicText with a single repetition, then after
        # superclasses are set up figure out how many repetitions are
        # needed to cover ``self.length`` and update the text
        # accordingly.
        MusicText.__init__(
            self,
            start,
            start_parent,
            text,
            font,
            brush,
            pen,
            background_brush=background_brush,
        )
        Spanner2D.__init__(self, end_pos, end_parent or self)
        self.rotation = self.angle
        single_repetition_chars = self.music_chars
        main_char_width = self._approx_width(single_repetition_chars)

        if start_cap_text:
            # Again need to hackily set temporary text value to work out the width
            self.text = start_cap_text
            start_cap_chars = self.music_chars
            start_cap_width = self.font.bounding_rect_of(self.text).width
        else:
            start_cap_chars = []
            start_cap_width = ZERO
        if end_cap_text:
            # Same idea...
            self.text = end_cap_text
            end_cap_chars = self.music_chars
            end_cap_width = self.font.bounding_rect_of(self.text).width
        else:
            end_cap_chars = []
            end_cap_width = ZERO
        main_reps_needed = round(
            cast(
                float,
                (self.spanner_2d_length - end_cap_width - start_cap_width)
                / main_char_width,
            )
        )
        # Now set the final resolved text
        self.music_chars = (
            start_cap_chars
            + (single_repetition_chars * main_reps_needed)
            + end_cap_chars
        )

    def _approx_width(self, chars: List[MusicChar]) -> Unit:
        # Try to hackily account for ligatures and variable advance widths by averaging
        # out the width of main chars repeated many times.
        reps = 20
        return (
            self.font.bounding_rect_of("".join(c.codepoint for c in chars) * reps).width
            / reps
        )
