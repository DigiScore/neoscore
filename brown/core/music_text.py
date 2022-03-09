from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple, Optional

from brown.core.mapping import Positioned
from brown.core.music_char import MusicChar
from brown.core.music_font import MusicFont
from brown.core.staff_object import StaffObject
from brown.core.text import Text
from brown.utils.point import Point, PointDef
from brown.utils.rect import Rect
from brown.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from brown.core.mapping import Parent


class _CachedTextGeometryKey(NamedTuple):
    text: str  # The key is the plain unicode text, not rich MusicChar list
    font: MusicFont
    scale: float


class _CachedTextGeometry(NamedTuple):
    bounding_rect: Rect


_GEOMETRY_CACHE: dict[_CachedTextGeometryKey, _CachedTextGeometry] = {}


class MusicText(Text):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.
    """

    # TODO MEDIUM find a way to type this text arg and/or simplify it
    def __init__(
        self,
        pos: PointDef,
        text: Any,
        parent: Parent,
        font: Optional[MusicFont] = None,
        scale: float = 1,
    ):
        """
        Args:
            pos: The position of the text.
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a either a `str`
                (glyph name), `tuple` (glyph name, alternate number),
                `MusicChar`, or a list of these.
            parent: The parent of the glyph. If no `font`
                is given, this must either be a `Staff` or an object which has
                a `Staff` as an ancestor.
            font: The music font to be used. If not specified,
                `parent` must be or have a `Staff` ancestor.
            scale: A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        if font is None:
            ancestor_staff = StaffObject.find_staff(parent)
            if ancestor_staff is None:
                raise ValueError(
                    "MusicText must be given either a MusicFont or an ancestor staff"
                )
            font = ancestor_staff.music_font
        self.music_chars = MusicText._resolve_music_chars(text, font)
        text = "".join(char.codepoint for char in self.music_chars)
        Text.__init__(self, pos, text, font, parent, scale=scale)

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        """The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.bounding_rect.width

    ######## PRIVATE PROPERTIES ########

    @property
    def bounding_rect(self) -> Rect:
        """The bounding rect for this text when rendered."""
        key = _CachedTextGeometryKey(self.text, self.font, self.scale)
        cached_result = _GEOMETRY_CACHE.get(key)
        if cached_result:
            return cached_result.bounding_rect
        bounding_rect = self._char_list_bounding_rect(self.music_chars)
        _GEOMETRY_CACHE[key] = _CachedTextGeometry(bounding_rect)
        return bounding_rect

    ######## PRIVATE METHODS ########

    def _char_list_bounding_rect(self, music_chars: list[MusicChar]) -> Rect:
        """Find the bounding rect of a given list of music chars.

        Takes a list of MusicChars and determined the bounding rect
        they would have if they were in this MusicText.

        The fonts of every music character should the the same as self.font.

        Args:
            music_chars: The string to represent

        Returns:
            The bounding rect of the specified text if drawn.

        Raises:
            ValueError: if `music_chars` is empty.
        """
        if not music_chars:
            raise ValueError(
                "Cannot find the bounding rect of an empty character sequence."
            )
        x = music_chars[0].glyph_info["glyphBBox"]["bBoxSW"][0]
        y = music_chars[0].glyph_info["glyphBBox"]["bBoxNE"][1]
        w = ZERO
        h = ZERO
        for char in music_chars:
            char_x = char.glyph_info["glyphBBox"]["bBoxSW"][0]
            char_y = char.glyph_info["glyphBBox"]["bBoxNE"][1]
            w += char.glyph_info["glyphBBox"]["bBoxNE"][0] - char_x
            h += (char.glyph_info["glyphBBox"]["bBoxSW"][1] - char_y) * -1
        return Rect(
            x * self.scale,
            y * self.scale,
            w * self.scale,
            h * self.scale,
        )

    @staticmethod
    def _resolve_music_chars(text: Any, font: MusicFont) -> list[MusicChar]:
        """
        Args:
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a either a `str`
                (glyph name), `tuple` (glyph name, alternate number),
                `MusicChar`, or a list of these.
            font: The font to be applied to the text
        """
        if isinstance(text, str):
            return [MusicChar(font, text)]
        elif isinstance(text, tuple):
            return [MusicChar(font, *text)]
        elif isinstance(text, MusicChar):
            return [text]
        elif isinstance(text, list):
            music_chars = []
            for music_char in text:
                if isinstance(music_char, str):
                    music_chars.append(MusicChar(font, music_char))
                elif isinstance(music_char, tuple):
                    music_chars.append(MusicChar(font, *music_char))
                elif isinstance(music_char, MusicChar):
                    music_chars.append(music_char)
                else:
                    raise TypeError
            return music_chars
        else:
            raise TypeError
