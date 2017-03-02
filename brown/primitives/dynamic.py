from brown.core.music_text_object import MusicTextObject


class DynamicStringError(Exception):

    """Exception raised when a dynamic string cannot be parsed."""

    def __init__(self, string, character):
        self.message = (
            'Cannot parse dynamic string "{}" - '
            'character "{}" unknown. '
            'Valid chars are: {}'
        ).format(string, character, list(Dynamic._dynamic_letter_map.keys()))
        super().__init__(self.message)


class Dynamic(MusicTextObject):

    """A textual dynamic marking"""

    # Map from letters to SMuFL canonical names
    _dynamic_letter_map = {
        'p': 'dynamicPiano',
        'm': 'dynamicMezzo',
        'f': 'dynamicForte',
        'r': 'dynamicRinforzando',
        's': 'dynamicSforzando',
        'z': 'dynamicZ',
        'n': 'dynamicNiente',
    }

    def __init__(self, pos, text, parent):
        """
        Args:
            pos (Point): The object position
            text (str): A valid dynamic indicator string consisting
                of the letters: 'p, m, f, r, s, z, n'
            parent (GraphicObject): The object parent.
        """
        parsed_text = self._parse_dynamic_string(text)
        MusicTextObject.__init__(self, pos, parsed_text, parent)

    ######## CONSTRUCTORS ########

    # ---- Convenience constructors ----

    @classmethod
    def ppp(cls, pos, parent):
        """Create a 'ppp' dynamic."""
        return cls(pos, 'ppp', parent)

    @classmethod
    def pp(cls, pos, parent):
        """Create a 'pp' dynamic."""
        return cls(pos, 'pp', parent)

    @classmethod
    def p(cls, pos, parent):
        """Create a 'p' dynamic."""
        return cls(pos, 'p', parent)

    @classmethod
    def mp(cls, pos, parent):
        """Create an 'mp' dynamic."""
        return cls(pos, 'mp', parent)

    @classmethod
    def mf(cls, pos, parent):
        """Create an 'mf' dynamic."""
        return cls(pos, 'mf', parent)

    @classmethod
    def f(cls, pos, parent):
        """Create a 'f' dynamic."""
        return cls(pos, 'f', parent)

    @classmethod
    def ff(cls, pos, parent):
        """Create a 'ff' dynamic."""
        return cls(pos, 'ff', parent)

    @classmethod
    def fff(cls, pos, parent):
        """Create a 'fff' dynamic."""
        return cls(pos, 'fff', parent)

    @classmethod
    def sfz(cls, pos, parent):
        """Create an 'sfz' dynamic."""
        return cls(pos, 'sfz', parent)

    @classmethod
    def fp(cls, pos, parent):
        """Create an 'fp' dynamic."""
        return cls(pos, 'fp', parent)

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
