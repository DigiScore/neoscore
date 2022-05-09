from __future__ import annotations

from typing import Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.western.accidental_type import AccidentalType


class Accidental(MusicText):

    """A visual accidental."""

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        accidental_type: AccidentalType | str,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: Position relative to ``parent``
            parent: If no font is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            accidental_type: Which accidental to draw. For extended accidentals,
                an arbitrary string SMuFL glyph name may be provided.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        self._accidental_type = accidental_type
        if isinstance(accidental_type, AccidentalType):
            canonical_name = accidental_type.value
        else:
            canonical_name = accidental_type
        MusicText.__init__(self, pos, parent, canonical_name, font)

    @property
    def accidental_type(self) -> AccidentalType | str:
        """The accidental variant.

        Can be set to either a standard accidental type or an
        arbitrary SMuFL glyph name.

        Setting this automatically updates the displayed glyph.
        """
        return self._accidental_type

    @accidental_type.setter
    def accidental_type(self, value: AccidentalType | str):
        self._accidental_type = value
        if isinstance(value, AccidentalType):
            self.text = value.value
        else:
            self.text = value
