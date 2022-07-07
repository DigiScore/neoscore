from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Union

from typing_extensions import TypeAlias

from neoscore.core.exceptions import InvalidPitchDescriptionError
from neoscore.western.accidental_type import AccidentalType


@dataclass(frozen=True)
class Pitch:

    """A written pitch with a letter, octave, and accidental.

    This class does not define an actual concert pitch, MIDI code, pitch class, etc.
    associated with it. Users building notation systems on it can decide whether this
    represents a concert pitch or a written one. Neoscore's ``western`` module treats it
    mostly as a written pitch, unconditionally writing provided accidentals regardless
    of context and key signatures.

    The class supports a helpful shorthand for standard western 12-EDO pitches inspired
    by Lilypond's pitch notation; see :obj:`.Pitch.from_str`.

    Extended accidentals are fully supported by passing arbitrary SMuFL glyph names to
    the ``accidental`` attribute.
    """

    _shorthand_regex = re.compile("^([a-g])(s|#|n|f|b|ss|x|ff|bb)?('*|,*)$")
    _diatonic_degrees_in_c = {"c": 1, "d": 2, "e": 3, "f": 4, "g": 5, "a": 6, "b": 7}
    _middle_c_octave = 4
    _accidental_shorthands = {
        "s": AccidentalType.SHARP,
        "#": AccidentalType.SHARP,
        "n": AccidentalType.NATURAL,
        "f": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "ss": AccidentalType.DOUBLE_SHARP,
        "x": AccidentalType.DOUBLE_SHARP,
        "ff": AccidentalType.DOUBLE_FLAT,
        "bb": AccidentalType.DOUBLE_FLAT,
    }

    letter: str
    """The a-g letter name of the pitch."""

    accidental: Optional[AccidentalType | str]
    """An accidental associated with the pitch.

    For conventional accidentals, this can be an ``AccidentalType``.
    Alternatively, this can be an arbitrary SMuFL glyph name string.
    """

    octave: int
    """The octave number, where 4 is the octave starting with middle-C."""

    @classmethod
    def from_str(cls, shorthand: str) -> Pitch:
        """Create a conventional Western ``Pitch`` from a string shorthand.

        The pitch shorthand is inspired by Lilypond's. It consists of three parts:
        a pitch letter, an optional accidental, and an optional octave mark.

        * Pitch letters are the standard ``c`` through ``b`` letters.
        * The accidental may be ``f`` or ``b`` for flat, ``s`` or ``#`` for sharp, ``n`` for
          natural, ``ss`` or ``x`` for double-sharp, and ``ff`` or ``bb`` for double-flat.
        * The octave indication is given by a series of apostrophes (``'``)
          or commas (``,``), where each apostrophe increases the pitch by an octave,
          and each comma decreases it. All octave transformations are relative to
          the octave starting at middle-C. The absence of an octave indicator means a
          pitch is within the octave starting at middle-C. (Note that this differs from
          Lilypond's notation, which starts at the octave *below* middle-C.)

        Some examples:

        * Middle-C: ``c``
        * The B directly below that: ``b,``
        * The C one octave below middle-C: ``c,``
        * The E-flat above middle-C: ``ef`` or ``eb``
        * The F-sharp above middle-C: ``fs`` or ``f#``
        * The G-double-sharp above middle-C: ``fx`` or ``fss``
        * The A-double-flat above the treble staff: ``aff'`` or ``abb'``

        """
        match = Pitch._shorthand_regex.match(shorthand)
        if match is None:
            raise InvalidPitchDescriptionError
        letter = match.group(1)
        accidental_str = match.group(2)
        ticks = match.group(3)
        letter = letter
        if accidental_str:
            accidental = Pitch._accidental_shorthands[accidental_str.lower()]
        else:
            accidental = None
        octave = 4
        if ticks:
            octave += len(ticks) * (-1 if ticks[0] == "," else 1)
        return Pitch(letter, accidental, octave)

    @classmethod
    def from_def(cls, pitch_def: PitchDef) -> Pitch:
        if isinstance(pitch_def, Pitch):
            return pitch_def
        elif isinstance(pitch_def, tuple):
            return Pitch(*pitch_def)
        return Pitch.from_str(pitch_def)

    @property
    def diatonic_degree_in_c(self) -> int:
        """The diatonic degree of the pitch as if it were in C.

        >>> Pitch.from_str("c").diatonic_degree_in_c
        1
        >>> Pitch.from_str("c'").diatonic_degree_in_c
        1
        >>> Pitch.from_str("d'''").diatonic_degree_in_c
        2
        >>> Pitch.from_str("bf,").diatonic_degree_in_c
        7
        """
        return Pitch._diatonic_degrees_in_c[self.letter]

    @property
    def staff_pos_from_middle_c(self) -> float:
        """The pitch's staff position relative to middle C.

        Values are in numeric pseudo-staff-units where positive
        values mean positions below middle C, and negative values
        mean positions above it.

        >>> Pitch.from_str("c").staff_pos_from_middle_c
        0
        >>> Pitch.from_str("cs").staff_pos_from_middle_c
        0
        >>> Pitch.from_str("d").staff_pos_from_middle_c
        -0.5
        >>> Pitch.from_str("d'").staff_pos_from_middle_c
        -4
        >>> Pitch.from_str("cn,,").staff_pos_from_middle_c
        7
        """
        middle_c = (4 * 7) + 1  # C at octave 4
        note_pos = (self.octave * 7) + self.diatonic_degree_in_c
        position = (note_pos - middle_c) / -2
        if position % 1 == 0:
            return int(position)
        else:
            return position


PitchDef: TypeAlias = Union[Pitch, str, tuple]
"""Shorthand for a ``Pitch``

May be either a ``Pitch``, a pitch string shorthand (see ``Pitch.from_str``), or a ``Pitch``
init arg tuple.
"""
