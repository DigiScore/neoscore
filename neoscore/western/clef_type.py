from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Union

KeySignatureLayout = Dict[str, tuple[float, float]]
"""A layout specification for accidentals in key signatures.

Instances should have a key for every pitch letter a-g (lowercase),
and each value should be an `(x, y)` tuple of pseudo staff positions
to be plugged into a staff's unit.
"""


@dataclass(frozen=True)
class ClefType:
    """A logical clef specifier.

    Many standard clefs are pre-defined in this module, but users can
    also create custom clef types using this class.
    """

    glyph_name: str
    """The SMuFL glyph name used to represent the clef."""

    staff_pos: float
    """Where the clef should be vertically drawn in a staff.

    This is given in pseudo staff units relative to the staff's top
    line. When positioning clefs, this should be passed into the
    staff's unit to find the appropriate y position.
    """

    middle_c_staff_pos: float
    """Where this clef places middle C in a staff.

    Like `staff_pos`, this is given in pseudo staff units relative to
    the staff's top line.
    """

    key_signature_flat_layout: Optional[KeySignatureLayout]
    """Set of positions for flat key sigantures, if applicable."""

    key_signature_sharp_layout: Optional[KeySignatureLayout]
    """Set of positions for sharp key sigantures, if applicable."""

    @classmethod
    def from_def(cls, clef_type_def: ClefTypeDef) -> ClefType:
        if isinstance(clef_type_def, ClefType):
            return clef_type_def
        return CLEF_TYPE_SHORTHAND_NAMES[clef_type_def.lower()]


_sharp_positions: KeySignatureLayout = {
    "f": (0, 0),
    "c": (1, 1.5),
    "g": (2, -0.5),
    "d": (3, 1),
    "a": (4, 2.5),
    "e": (5, 0.5),
    "b": (6, 2),
}
_flat_positions: KeySignatureLayout = {
    "b": (0, 2),
    "e": (1, 0.5),
    "a": (2, 2.5),
    "d": (3, 1),
    "g": (4, 3),
    "c": (5, 1.5),
    "f": (6, 3.5),
}
_bass_flat_positions = {
    key: (value[0], value[1] + 1) for key, value in _flat_positions.items()
}
_tenor_flat_positions = {
    key: (value[0], value[1] - 0.5) for key, value in _flat_positions.items()
}
_alto_flat_positions = {
    key: (value[0], value[1] + 0.5) for key, value in _flat_positions.items()
}
_bass_sharp_positions = {
    key: (value[0], value[1] + 1) for key, value in _sharp_positions.items()
}
_tenor_sharp_positions = {
    "f": (0, 3),
    "c": (1, 1),
    "g": (2, 2.5),
    "d": (3, 0.5),
    "a": (4, 2),
    "e": (5, 0),
    "b": (6, 1.5),
}
_alto_sharp_positions = {
    key: (value[0], value[1] + 0.5) for key, value in _sharp_positions.items()
}


TREBLE = ClefType("gClef", 3, 5, _flat_positions, _sharp_positions)
TREBLE_8VB = ClefType("gClef8vb", 3, 1.5, _flat_positions, _sharp_positions)
BASS = ClefType("fClef", 1, -1, _bass_flat_positions, _bass_sharp_positions)
BASS_8VB = ClefType("fClef8vb", 1, -4.5, _bass_flat_positions, _bass_sharp_positions)
TENOR = ClefType("cClef", 1, 1, _tenor_flat_positions, _tenor_sharp_positions)
ALTO = ClefType("cClef", 2, 2, _alto_flat_positions, _alto_sharp_positions)

PERCUSSION_1 = ClefType(
    "unpitchedPercussionClef1", 2, 2, _alto_flat_positions, _alto_sharp_positions
)
"""Percussion clef consisting of 2 solid bars.

Percussion clefs placed in staves are treated as alto clefs.
"""

PERCUSSION_2 = ClefType(
    "unpitchedPercussionClef2", 2, 2, _alto_flat_positions, _alto_sharp_positions
)
"""Percussion clef consisting of an open rectangle.

Percussion clefs placed in staves are treated as alto clefs.
"""

CLEF_TYPE_SHORTHAND_NAMES = {
    "treble": TREBLE,
    "treble_8vb": TREBLE_8VB,
    "bass": BASS,
    "bass_8vb": BASS_8VB,
    "tenor": TENOR,
    "alto": ALTO,
    "percussion_1": PERCUSSION_1,
    "percussion_2": PERCUSSION_2,
}

ClefTypeDef = Union[ClefType, str]
"""ClefTypes can be given by the string name of any pre-defined ClefType in this module.

String lookup is case-insensitive.
"""
