from __future__ import annotations

from typing import Optional

from neoscore.core.exceptions import DynamicStringError
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject


class Dynamic(MusicText):

    """A textual dynamic marking"""

    # Map from letters to SMuFL canonical names
    _dynamic_letter_map = {
        "p": "dynamicPiano",
        "m": "dynamicMezzo",
        "f": "dynamicForte",
        "r": "dynamicRinforzando",
        "s": "dynamicSforzando",
        "z": "dynamicZ",
        "n": "dynamicNiente",
    }

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        text: str,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: Position relative to ``parent``
            parent: If no font is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            text: A valid dynamic indicator string consisting
                of the letters: 'p, m, f, r, s, z, n'
            font: If provided, this overrides any font found in the ancestor chain.
        """
        parsed_text = self._parse_dynamic_string(text)
        MusicText.__init__(self, pos, parent, parsed_text, font)

    @classmethod
    def ppp(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'ppp' dynamic."""
        return cls(pos, parent, "ppp", font)

    @classmethod
    def pp(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'pp' dynamic."""
        return cls(pos, parent, "pp", font)

    @classmethod
    def p(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'p' dynamic."""
        return cls(pos, parent, "p", font)

    @classmethod
    def mp(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create an 'mp' dynamic."""
        return cls(pos, parent, "mp", font)

    @classmethod
    def mf(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create an 'mf' dynamic."""
        return cls(pos, parent, "mf", font)

    @classmethod
    def f(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'f' dynamic."""
        return cls(pos, parent, "f", font)

    @classmethod
    def ff(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'ff' dynamic."""
        return cls(pos, parent, "ff", font)

    @classmethod
    def fff(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create a 'fff' dynamic."""
        return cls(pos, parent, "fff", font)

    @classmethod
    def sfz(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create an 'sfz' dynamic."""
        return cls(pos, parent, "sfz", font)

    @classmethod
    def fp(
        cls, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ) -> Dynamic:
        """Create an 'fp' dynamic."""
        return cls(pos, parent, "fp", font)

    @classmethod
    def _parse_dynamic_string(cls, string: str) -> List[str]:
        """Parse a dynamics string into a list of SMuFL canonical names"""
        music_chars = []
        for char in string:
            try:
                music_chars.append(cls._dynamic_letter_map[char])
            except KeyError:
                raise DynamicStringError(string, char)
        return music_chars
