from neoscore.core.music_text import MusicText
from neoscore.core.painted_object import PaintedObject
from neoscore.core.staff_object import StaffObject
from neoscore.utils.exceptions import DynamicStringError
from neoscore.utils.point import PointDef


class Dynamic(MusicText, StaffObject):

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

    def __init__(self, pos: PointDef, parent: PaintedObject, text: str):
        """
        Args:
            pos: The object position
            parent: The object parent.
            text: A valid dynamic indicator string consisting
                of the letters: 'p, m, f, r, s, z, n'
        """
        parsed_text = self._parse_dynamic_string(text)
        MusicText.__init__(self, pos, parent, parsed_text)
        StaffObject.__init__(self, parent)

    ######## CONSTRUCTORS ########

    # ---- Convenience constructors ----

    @classmethod
    def ppp(cls, pos, parent):
        """Create a 'ppp' dynamic."""
        return cls(pos, parent, "ppp")

    @classmethod
    def pp(cls, pos, parent):
        """Create a 'pp' dynamic."""
        return cls(pos, parent, "pp")

    @classmethod
    def p(cls, pos, parent):
        """Create a 'p' dynamic."""
        return cls(pos, parent, "p")

    @classmethod
    def mp(cls, pos, parent):
        """Create an 'mp' dynamic."""
        return cls(pos, parent, "mp")

    @classmethod
    def mf(cls, pos, parent):
        """Create an 'mf' dynamic."""
        return cls(pos, parent, "mf")

    @classmethod
    def f(cls, pos, parent):
        """Create a 'f' dynamic."""
        return cls(pos, parent, "f")

    @classmethod
    def ff(cls, pos, parent):
        """Create a 'ff' dynamic."""
        return cls(pos, parent, "ff")

    @classmethod
    def fff(cls, pos, parent):
        """Create a 'fff' dynamic."""
        return cls(pos, parent, "fff")

    @classmethod
    def sfz(cls, pos, parent):
        """Create an 'sfz' dynamic."""
        return cls(pos, parent, "sfz")

    @classmethod
    def fp(cls, pos, parent):
        """Create an 'fp' dynamic."""
        return cls(pos, parent, "fp")

    ######## PRIVATE METHODS ########

    @classmethod
    def _parse_dynamic_string(cls, string):
        """Parse a dynamics string into a list of SMuFL canonical names

        Returns: list[MusicChar]
        """
        music_chars = []
        for char in string:
            try:
                music_chars.append(cls._dynamic_letter_map[char])
            except KeyError:
                raise DynamicStringError(string, char)
        return music_chars
