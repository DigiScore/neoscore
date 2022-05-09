from enum import Enum
from typing import Optional


class AccidentalType(Enum):

    """A logical accidental descriptor covering standard 12-EDO western accidentals.

    These are used both in abstract :obj:`.Pitch` descriptions and in concrete
    graphical :obj:`.Accidental` objects.

    Each enum's string value is its corresponding canonical SMuFL glyph name.

    Not all glyphs are mandatory in SMuFL, but all are available in Bravura.
    """

    FLAT = "accidentalFlat"

    NATURAL = "accidentalNatural"

    SHARP = "accidentalSharp"

    DOUBLE_FLAT = "accidentalDoubleFlat"

    DOUBLE_SHARP = "accidentalDoubleSharp"

    NATURAL_FLAT = "accidentalNaturalFlat"

    NATURAL_SHARP = "accidentalNaturalSharp"

    FLAT_SMALL = "accidentalFlatSmall"

    NATURAL_SMALL = "accidentalNaturalSmall"

    SHARP_SMALL = "accidentalSharpSmall"

    FLAT_PARENS = "accidentalFlatParens"

    NATURAL_PARENS = "accidentalNaturalParens"

    SHARP_PARENS = "accidentalSharpParens"

    DOUBLE_SHARP_PARENS = "accidentalDoubleSharpParens"

    DOUBLE_FLAT_PARENS = "accidentalDoubleFlatParens"

    @property
    def pitch_class_offset(self) -> Optional[int]:
        """Return an integer pitch class offset if applicable.

        This will return ``None`` for all accidental types except standard 12-EDO ones.
        """
        return _offset_map.get(self, None)


_offset_map = {
    AccidentalType.FLAT: -1,
    AccidentalType.NATURAL: 0,
    AccidentalType.SHARP: 1,
    AccidentalType.DOUBLE_FLAT: -2,
    AccidentalType.DOUBLE_SHARP: 2,
    AccidentalType.NATURAL_FLAT: 0,
    AccidentalType.NATURAL_SHARP: 1,
    AccidentalType.FLAT_SMALL: -1,
    AccidentalType.NATURAL_SMALL: 0,
    AccidentalType.SHARP_SMALL: 1,
    AccidentalType.FLAT_PARENS: -1,
    AccidentalType.NATURAL_PARENS: 0,
    AccidentalType.SHARP_PARENS: 1,
    AccidentalType.DOUBLE_SHARP_PARENS: 2,
    AccidentalType.DOUBLE_FLAT_PARENS: -2,
}
