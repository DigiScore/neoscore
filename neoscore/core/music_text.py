from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple, Optional

from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.staff_object import StaffObject
from neoscore.core.text import Text
from neoscore.utils.point import PointDef
from neoscore.utils.rect import Rect
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


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
    def __init__(self, pos: PointDef, parent: Parent, text: Any, font: Optional[MusicFont] = None, scale: float = 1):
        """
        Args:
            pos: The position of the text.
            parent: The parent of the glyph. If no `font`
                is given, this must either be a `Staff` or an object which has
                a `Staff` as an ancestor.
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a either a `str`
                (glyph name), `tuple` (glyph name, alternate number),
                `MusicChar`, or a list of these. Empty text will fail.
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
        self._music_chars = MusicText._resolve_music_chars(text, font)
        resolved_str = MusicText._music_chars_to_str(self._music_chars)
        Text.__init__(self, pos, parent, resolved_str, font, scale=scale)

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        """The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.bounding_rect.width

    @property
    def music_chars(self) -> list[MusicChar]:
        """A list of the SMuFL characters in the string including metadata.

        If set, this will also update `self.text`.
        """
        return self._music_chars

    @music_chars.setter
    def music_chars(self, value: list[MusicChar]):
        self._music_chars = value
        self._text = MusicText._music_chars_to_str(value)

    @property
    def text(self) -> str:
        """The raw unicode representation of the SMuFL text.

        If set, this will also update `self.music_chars`
        """
        return self._text

    @text.setter
    # TODO MEDIUM when typing music text args update here as well
    def text(self, value):
        self._music_chars = MusicText._resolve_music_chars(value, self.font)
        resolved_str = MusicText._music_chars_to_str(self._music_chars)
        self._text = resolved_str

    ######## PRIVATE PROPERTIES ########

    @property
    def bounding_rect(self) -> Rect:
        """The bounding rect for this text when rendered."""
        key = _CachedTextGeometryKey(self.text, self.font, self.scale)
        cached_result = _GEOMETRY_CACHE.get(key)
        if cached_result:
            return cached_result.bounding_rect
        bounding_rect = self.font.bounding_rect_of(self.text) * self.scale
        _GEOMETRY_CACHE[key] = _CachedTextGeometry(bounding_rect)
        return bounding_rect

    ######## PRIVATE METHODS ########

    @staticmethod
    def _music_chars_to_str(music_chars: list[MusicChar]) -> str:
        return "".join(char.codepoint for char in music_chars)

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
