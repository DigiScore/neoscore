from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.models.beat import Beat, BeatDef
from neoscore.utils.point import Point
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class TimeSignature(ObjectGroup, HasMusicFont):

    """A logical and graphical time signature

    TODO LOW: Time signatures with differing character-length numerators and
    denominators (e.g. 12/8) currently display incorrectly as left-justified.
    """

    _glyph_names = {
        1: "timeSig1",
        2: "timeSig2",
        3: "timeSig3",
        4: "timeSig4",
        5: "timeSig5",
        6: "timeSig6",
        7: "timeSig7",
        8: "timeSig8",
        9: "timeSig9",
    }

    def __init__(
        self,
        pos_x: Unit,
        parent: Parent,
        meter: BeatDef,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos_x: The x position relative to the
                parent staff
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            meter: The length of a measure in this
                time signature. The numerator and denominators
                of this duration are used literally as the numbers
                in the rendered representation of the signature.
                While a 6/8 measure will take the same amount of time
                as a 3/4 measure, the representations (and note groupings)
                are different.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        ObjectGroup.__init__(self, Point(pos_x, ZERO), parent)
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font
        # TODO LOW error if this beat is a nested tuplet
        self._meter = Beat.from_def(meter)
        # Add one glyph for each digit
        self._numerator_glyph = MusicText(
            (ZERO, font.unit(1)),
            self,
            TimeSignature._glyphs_for_number(self.meter.fraction.numerator),
        )
        self._denominator_glyph = MusicText(
            (ZERO, font.unit(3)),
            self,
            TimeSignature._glyphs_for_number(self.meter.fraction.denominator),
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def numerator_glyph(self) -> MusicText:
        """MusicText: The upper glyph for the time signature"""
        return self._numerator_glyph

    @property
    def denominator_glyph(self) -> MusicText:
        """MusicText: The lower glyph for the time signature"""
        return self._denominator_glyph

    @property
    def meter(self) -> Beat:
        """Beat: The length of one bar in this time signature"""
        return self._meter

    ######## PRIVATE METHODS  ########

    @staticmethod
    def _glyphs_for_number(number: int) -> list[str]:
        """Convert time signature number to a list of SMuFL glyph names."""
        return [TimeSignature._glyph_names[int(digit)] for digit in str(number)]
