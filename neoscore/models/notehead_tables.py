"""Tables of glyphs for common notehead styles

This module includes prebuilt `NoteheadTable`s for many notehead
flavors included in SMuFL. Custom tables using arbitrary SMuFL glyphs
may also be created by simply instantiating a `NoteheadTable` and
passing it wherever needed.

Note that many of the more obscure glyph tables only have a solid and
empty variant, for example `MOON`. In these cases, the empty glyph is
used for all except the `short` key, for which the solid glyph is
used.
"""

from dataclasses import dataclass

from neoscore.models.notehead_duration import NoteheadDuration

# NOTE: When creating a new table, be sure to add it to ALL_TABLES at
# the end of this file.


@dataclass(frozen=True)
class NoteheadTable:
    """A mapping from duration classes to canonical SMuFL glyph names."""

    double_whole: str
    whole: str
    half: str
    short: str
    """Quarter notes and shorter"""

    def lookup_duration(self, dur: NoteheadDuration) -> str:
        if dur == NoteheadDuration.SHORT:
            return self.short
        elif dur == NoteheadDuration.HALF:
            return self.half
        elif dur == NoteheadDuration.WHOLE:
            return self.whole
        elif dur == NoteheadDuration.DOUBLE_WHOLE:
            return self.double_whole
        else:
            raise ValueError(f"Unknown notehead duration: {dur}")


STANDARD = NoteheadTable(
    "noteheadDoubleWhole", "noteheadWhole", "noteheadHalf", "noteheadBlack"
)

STANDARD_WITH_PARENTHESES = NoteheadTable(
    "noteheadDoubleWholeParens",
    "noteheadWholeParens",
    "noteheadHalfParens",
    "noteheadBlackParens",
)

STANDARD_SMALL = NoteheadTable(
    "noteheadDoubleWholeSmall",
    "noteheadWholeSmall",
    "noteheadHalfSmall",
    "noteheadBlackSmall",
)

X = NoteheadTable(
    "noteheadXDoubleWhole", "noteheadXWhole", "noteheadXHalf", "noteheadXBlack"
)

PLUS = NoteheadTable(
    "noteheadPlusDoubleWhole",
    "noteheadPlusWhole",
    "noteheadPlusHalf",
    "noteheadPlusBlack",
)

CIRCLE_X = NoteheadTable(
    "noteheadCircleXDoubleWhole",
    "noteheadCircleXWhole",
    "noteheadCircleXHalf",
    "noteheadCircleX",
)

STANDARD_WITH_X = NoteheadTable(
    "noteheadDoubleWholeWithX",
    "noteheadWholeWithX",
    "noteheadHalfWithX",
    "noteheadVoidWithX",
)

SQUARE = NoteheadTable(
    "noteheadSquareWhite",
    "noteheadSquareWhite",
    "noteheadSquareWhite",
    "noteheadSquareBlack",
)

TRIANGLE_UP = NoteheadTable(
    "noteheadTriangleUpDoubleWhole",
    "noteheadTriangleUpWhole",
    "noteheadTriangleUpHalf",
    "noteheadTriangleUpBlack",
)

TRIANGLE_LEFT = NoteheadTable(
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftBlack",
)

TRIANGLE_RIGHT = NoteheadTable(
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightBlack",
)

TRIANGLE_DOWN = NoteheadTable(
    "noteheadTriangleDownDoubleWhole",
    "noteheadTriangleDownWhole",
    "noteheadTriangleDownHalf",
    "noteheadTriangleDownBlack",
)

TRIANGLE_UP_RIGHT = NoteheadTable(
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightBlack",
)

TRIANGLE_ROUND_DOWN = NoteheadTable(
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownBlack",
)

MOON = NoteheadTable(
    "noteheadMoonWhite",
    "noteheadMoonWhite",
    "noteheadMoonWhite",
    "noteheadMoonBlack",
)

PARENTHESIS = NoteheadTable(
    "noteheadParenthesis",
    "noteheadParenthesis",
    "noteheadParenthesis",
    "noteheadParenthesis",
)
"""An empty set of parentheses in place of noteheads. All four glyphs are the same."""

STANDARD_WITH_SLASH_UP = NoteheadTable(
    "noteheadSlashedDoubleWhole1",
    "noteheadSlashedWhole1",
    "noteheadSlashedHalf1",
    "noteheadSlashedBlack1",
)
"""Standard noteheads with slashes going from bottom left to top right."""

STANDARD_WITH_SLASH_DOWN = NoteheadTable(
    "noteheadSlashedDoubleWhole2",
    "noteheadSlashedWhole2",
    "noteheadSlashedHalf2",
    "noteheadSlashedBlack2",
)
"""Standard noteheads with slashes going from top left to bottom right."""

DIAMOND = NoteheadTable(
    "noteheadDiamondDoubleWhole",
    "noteheadDiamondWhole",
    "noteheadDiamondHalf",
    "noteheadDiamondBlack",
)

DIAMOND_WIDE = NoteheadTable(
    "noteheadDiamondDoubleWhole",
    "noteheadDiamondWhole",
    "noteheadDiamondHalfWide",
    "noteheadDiamondBlackWide",
)
"""Like `DIAMOND` but with wider half and short variants"""

DIAMOND_OLD = NoteheadTable(
    "noteheadDiamondDoubleWholeOld",
    "noteheadDiamondWholeOld",
    "noteheadDiamondHalfOld",
    "noteheadDiamondBlackOld",
)

STANDARD_CIRCLED = NoteheadTable(
    "noteheadCircledDoubleWhole",
    "noteheadCircledWhole",
    "noteheadCircledHalf",
    "noteheadCircledBlack",
)

STANDARD_LARGE_CIRCLED = NoteheadTable(
    "noteheadCircledDoubleWholeLarge",
    "noteheadCircledWholeLarge",
    "noteheadCircledHalfLarge",
    "noteheadCircledBlackLarge",
)
"""Like `STANDARD_CIRCLED` but with a larger circle"""

LARGE_ARROW_UP = NoteheadTable(
    "noteheadLargeArrowUpDoubleWhole",
    "noteheadLargeArrowUpWhole",
    "noteheadLargeArrowUpHalf",
    "noteheadLargeArrowUpBlack",
)

LARGE_ARROW_DOWN = NoteheadTable(
    "noteheadLargeArrowDownDoubleWhole",
    "noteheadLargeArrowDownWhole",
    "noteheadLargeArrowDownHalf",
    "noteheadLargeArrowDownBlack",
)

ALL_TABLES: list[NoteheadTable] = [
    STANDARD,
    STANDARD_WITH_PARENTHESES,
    STANDARD_SMALL,
    X,
    PLUS,
    CIRCLE_X,
    STANDARD_WITH_X,
    SQUARE,
    TRIANGLE_UP,
    TRIANGLE_LEFT,
    TRIANGLE_RIGHT,
    TRIANGLE_DOWN,
    TRIANGLE_UP_RIGHT,
    TRIANGLE_ROUND_DOWN,
    MOON,
    PARENTHESIS,
    STANDARD_WITH_SLASH_UP,
    STANDARD_WITH_SLASH_DOWN,
    DIAMOND,
    DIAMOND_WIDE,
    DIAMOND_OLD,
    STANDARD_CIRCLED,
    STANDARD_LARGE_CIRCLED,
    LARGE_ARROW_UP,
    LARGE_ARROW_DOWN,
]
"""A list of all the notehead tables in this module"""
