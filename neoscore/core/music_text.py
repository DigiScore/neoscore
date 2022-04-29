from __future__ import annotations

from typing import NamedTuple, Optional, Type, TypeAlias, Union, cast

from neoscore.core.brush import BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_char import MusicChar, MusicCharDef
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rect import Rect
from neoscore.core.text import Text
from neoscore.core.units import Unit


class _CachedTextGeometryKey(NamedTuple):
    text: str  # The key is the plain unicode text, not rich MusicChar list
    font: MusicFont
    scale: float


class _CachedTextGeometry(NamedTuple):
    bounding_rect: Rect


_GEOMETRY_CACHE: dict[_CachedTextGeometryKey, _CachedTextGeometry] = {}


MusicStringDef: TypeAlias = Union[MusicCharDef, list[MusicCharDef]]
"""Argument specifying SMuFL ``MusicText`` strings.

This supports several forms for different use-cases. The most commonly
used form is a simple SMuFL canonical glyph name.
* A canonical SMuFL glyph name. This may be an empty string to indicate 0-length text.
* A tuple of a glyph name and a SMuFL alternate number.
* A fully defined ``MusicChar``.
* A list of any of these, including an empty list.
"""


class MusicText(Text, HasMusicFont):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        text: MusicStringDef,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        scale: float = 1,
        rotation: float = 0,
        background_brush: Optional[BrushDef] = None,
        z_index: int = 0,
        breakable: bool = True,
        centered_x: bool = False,
        centered_y: bool = False,
    ):
        """
        Args:
            pos: The position of the text.
            parent: The parent of the glyph. If no ``font`` is given,
                this or one of its ancestors must implement ``HasMusicFont``.
            text: The text to display. Can be given as a SMuFL glyph name,
                or other shorthand forms. See ``MusicStringDef`` and ``MusicCharDef``.
            font: The music font to be used. If not specified,
                ``parent`` must be or have a ``Staff`` ancestor.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            scale: A scaling factor to be applied
                in addition to the size of the music font.
            rotation: Angle in degrees. Note that breakable rotated text is
                not currently supported.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
            z_index: Controls draw order with higher values drawn first.
            breakable: Whether this object should break across lines in
                Flowable containers.
            centered_x: Whether to horizontally center the text at the given position.
                Note that centered text which breaks across flowable lines is not yet
                supported and will display incorrectly.
            centered_y: Whether to vertically center the text at the given position.
        """
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_chars = MusicText._resolve_music_chars(font, text)
        resolved_str = MusicText._music_chars_to_str(self._music_chars)
        Text.__init__(
            self,
            pos,
            parent,
            resolved_str,
            font,
            brush,
            pen,
            scale,
            rotation,
            background_brush,
            z_index,
            breakable,
            centered_x,
            centered_y,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def music_chars(self) -> list[MusicChar]:
        """A list of the SMuFL characters in the string including metadata.

        If set, this will also update ``self.text``.
        """
        return self._music_chars

    @music_chars.setter
    def music_chars(self, value: list[MusicChar]):
        self._music_chars = value
        self._text = MusicText._music_chars_to_str(value)

    @property
    def text(self) -> str:
        """The raw unicode representation of the SMuFL text.

        If set, this will also update ``self.music_chars``
        """
        return self._text

    @text.setter
    def text(self, value: MusicStringDef):
        self._music_chars = MusicText._resolve_music_chars(self.music_font, value)
        resolved_str = MusicText._music_chars_to_str(self._music_chars)
        self._text = resolved_str

    @property
    def music_font(self) -> MusicFont:
        """The SMuFL font used in this text.

        This is an expressive synonym for the ``font`` field which implements the
        ``HasMusicFont`` mixin.
        """
        return cast(MusicFont, self._font)

    @music_font.setter
    def music_font(self, value: MusicFont):
        self._font = value

    @property
    def unit(self) -> Type[Unit]:
        return self.music_font.unit

    @property
    def _raw_scaled_bounding_rect(self) -> Rect:
        key = _CachedTextGeometryKey(self.text, self.music_font, self.scale)
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
    def _resolve_music_chars(font: MusicFont, text: MusicStringDef) -> list[MusicChar]:
        if isinstance(text, list):
            music_chars = []
            for text_char in text:
                char = MusicText._resolve_single_music_char(
                    font, cast(MusicCharDef, text_char)
                )
                if char is not None:
                    music_chars.append(char)
            return music_chars
        else:
            char = MusicText._resolve_single_music_char(font, text)
            if char is None:
                return []
            else:
                return [char]

    @staticmethod
    def _resolve_single_music_char(
        font: MusicFont, char: MusicCharDef
    ) -> Optional[MusicChar]:
        if isinstance(char, str):
            if char:
                return MusicChar(font, char)
            else:
                return None
        elif isinstance(char, tuple):
            return MusicChar(font, *char)
        elif isinstance(char, MusicChar):
            return char
        else:
            raise TypeError
