from __future__ import annotations

from typing import Optional

from neoscore.core.font import Font
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicStringDef, MusicText
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.raw_music_char import RawMusicChar
from neoscore.core.text import Text
from neoscore.core.units import ZERO


class MetronomeMark(PositionedObject, HasMusicFont):
    """A combined :obj:`MusicText` and :obj:`Text` for use in metronome markings"""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        music_str: MusicStringDef,
        text_str: str,
        music_font: Optional[MusicFont] = None,
        text_font: Optional[Font] = None,
        spaces_between_music_chars: bool = True,
    ):
        """
        Args:
            pos: Position relative to ``parent``
            parent: If no ``music_font`` is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            music_str: The :obj:`MusicText` string portion of the mark. Glyphs should
                typically come from `the relevant SMuFL range
                <https://w3c.github.io/smufl/latest/tables/metronome-marks.html>`_.
            text_str: The plain-text string portion of the mark. This will typically
                be of the form "= 123".
            music_font: If provided, this overrides any music font found in the
                ancestor chain.
            text_font: The font for the plain text portion of the mark.
            spaces_between_music_chars: Whether to insert spaces between each specified
                music character. This is needed to correctly space rhythm dots if used.
        """
        PositionedObject.__init__(self, pos, parent)
        self._music_font = music_font or HasMusicFont.find_music_font(parent)
        self._music_text_obj = MusicText(ORIGIN, self, music_str, self._music_font)
        if spaces_between_music_chars and len(self._music_text_obj.music_chars) > 1:
            self._music_text_obj.music_chars = self._insert_spaces(
                self._music_text_obj.music_chars
            )
        music_text_rect = self._music_text_obj.bounding_rect
        music_text_end_x = music_text_rect.x + music_text_rect.width
        # Because text objects can't have leading or trailing spaces, to get a space
        # between these elements we do a terrible hack to find the width of a space and
        # offset accordingly. See https://github.com/DigiScore/neoscore/issues/34
        text_obj = Text((music_text_end_x, ZERO), self, " " + text_str, text_font)
        width_including_space = text_obj.bounding_rect.width
        text_obj.text = text_str
        text_obj.x += width_including_space - text_obj.bounding_rect.width
        self._plain_text_obj = text_obj

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def music_text_obj(self) -> MusicText:
        return self._music_text_obj

    @property
    def plain_text_obj(self) -> Text:
        return self._plain_text_obj

    def _insert_spaces(self, chars: List[MusicChar]) -> List[MusicChar]:
        result = []
        blank = RawMusicChar(self.music_font, " ")
        for i, char in enumerate(chars):
            result.append(char)
            if i < len(chars) - 1:
                result.append(blank)
        return result
