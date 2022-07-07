from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple, Union, cast

from typing_extensions import TypeAlias

_glyph_names = {
    0: "timeSig0",
    1: "timeSig1",
    2: "timeSig2",
    3: "timeSig3",
    4: "timeSig4",
    5: "timeSig5",
    6: "timeSig6",
    7: "timeSig7",
    8: "timeSig8",
    9: "timeSig9",
}


@dataclass(frozen=True)
class Meter:
    """A time signature graphical meter comprising two lists of glyphs.

    Users are recommended to use the ``Meter.numeric()`` constructor,
    which provides a convenient way to create standard meters. The
    direct constructor is mostly useful for writing more exotic
    meters, supporting arbitrary glyphs.

    If only a single line of text is needed for the meter (as with the
    common time "C"), it should go in ``upper_text_glyph_names`` and
    ``lower_text_glyph_names`` should be left empty.

    """

    upper_text_glyph_names: List[str]
    lower_text_glyph_names: List[str]

    @classmethod
    def numeric(cls, upper: Union[int | List[int]], lower: int) -> Meter:
        """Create a meter with upper and lower numbers.

        The upper number can be a single number, or a list of them.

        Lists of numbers will be treated as additive time signatures
        where each upper number is joined by a plus sign. This is
        useful for time signatures like ``[3 + 2 + 3] / 8``.
        """
        if isinstance(upper, int):
            upper_glyphs = Meter._glyphs_for_number(upper)
        else:
            upper_glyphs = reduce(
                lambda a, b: a + ["timeSigPlus"] + b,
                [Meter._glyphs_for_number(number) for number in upper],
            )
        lower_glyphs = Meter._glyphs_for_number(lower)
        return Meter(upper_glyphs, lower_glyphs)

    @classmethod
    def from_def(cls, meter_def: MeterDef) -> Meter:
        if isinstance(meter_def, tuple):
            return Meter.numeric(*meter_def)
        return cast(Meter, meter_def)

    @staticmethod
    def _glyphs_for_number(number: int) -> List[str]:
        return [_glyph_names[int(digit)] for digit in str(number)]


COMMON_TIME = Meter(["timeSigCommon"], [])
CUT_TIME = Meter(["timeSigCutCommon"], [])


MeterDef: TypeAlias = Union[Meter, Tuple[Union[int, List[int]], int]]
"""Shorthand for Meter.

Either a Meter, or an argument tuple for ``Meter.numeric``.
"""
