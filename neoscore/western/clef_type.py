from __future__ import annotations

from dataclasses import dataclass
from typing import Union


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

    @classmethod
    def from_def(cls, clef_type_def: ClefTypeDef) -> ClefType:
        if isinstance(clef_type_def, ClefType):
            return clef_type_def
        return CLEF_TYPE_SHORTHAND_NAMES[clef_type_def.lower()]


TREBLE = ClefType("gClef", 3, 5)
TREBLE_8VB = ClefType("gClef8vb", 3, 1.5)
BASS = ClefType("fClef", 1, -1)
BASS_8VB = ClefType("fClef8vb", 1, -4.5)
TENOR = ClefType("cClef", 1, 1)
ALTO = ClefType("cClef", 2, 2)

PERCUSSION_1 = ClefType("unpitchedPercussionClef1", 2, 2)
"""Percussion clef consisting of 2 solid bars.

Percussion clefs placed in staves are treated as alto clefs.
"""

PERCUSSION_2 = ClefType("unpitchedPercussionClef2", 2, 2)
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
