from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.utils.point import Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western.meter import Meter, MeterDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class TimeSignature(ObjectGroup, HasMusicFont):

    """A logical and graphical time signature

    TODO LOW: Time signatures with differing character-length numerators and
    denominators (e.g. 12/8) currently display incorrectly as left-justified.
    """

    def __init__(
        self,
        pos_x: Unit,
        parent: Parent,
        meter: MeterDef,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos_x: The x position relative to the
                parent staff
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            meter: The meter represented.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        ObjectGroup.__init__(self, Point(pos_x, ZERO), parent)
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font
        self._meter = Meter.from_def(meter)
        # Add one glyph for each digit
        self._upper_text = MusicText(
            (ZERO, font.unit(1)),
            self,
            self.meter.upper_text_glyph_names,
        )
        self._lower_text = MusicText(
            (ZERO, font.unit(3)),
            self,
            self.meter.lower_text_glyph_names,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def upper_text(self) -> MusicText:
        """MusicText: The upper glyph for the time signature"""
        return self._upper_text

    @property
    def lower_text(self) -> MusicText:
        """MusicText: The lower glyph for the time signature"""
        return self._lower_text

    @property
    def meter(self) -> Meter:
        """The meter represented.

        Setting this will automatically update the time signature's glyphs.
        """
        return self._meter

    @meter.setter
    def meter(self, value: MeterDef):
        self._meter = Meter.from_def(value)
        self.upper_text.text = self._meter.upper_text_glyph_names
        self.lower_text.text = self._meter.lower_text_glyph_names
