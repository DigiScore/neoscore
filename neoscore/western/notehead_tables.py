"""Tables of glyphs for common notehead styles
This module includes prebuilt ``NoteheadTable``\ s for many notehead
flavors included in SMuFL. Custom tables using arbitrary SMuFL glyphs
may also be created by simply instantiating a ``NoteheadTable`` and
passing it wherever needed.

Note that many of the more obscure glyph tables only have a solid and
empty variant, for example ``MOON``. In these cases, the empty glyph is
used for all except the ``short`` key, for which the solid glyph is
used.
"""

from dataclasses import dataclass
from typing import List

from neoscore.western.duration_display import BaseDuration

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

    def lookup_duration(self, base_division: BaseDuration) -> str:
        """Given a base division, return the required glyph to represent it.

        Assumes ``base_division`` is 0 or a power of 2.
        """
        if base_division >= 4:
            return self.short
        elif base_division == 2:
            return self.half
        elif base_division == 1:
            return self.whole
        else:
            return self.double_whole


STANDARD = NoteheadTable(
    "noteheadDoubleWhole", "noteheadWhole", "noteheadHalf", "noteheadBlack"
)
"""Standard western notation noteheads"""

STANDARD_WITH_PARENTHESES = NoteheadTable(
    "noteheadDoubleWholeParens",
    "noteheadWholeParens",
    "noteheadHalfParens",
    "noteheadBlackParens",
)
"""Standard noteheads enclosed in parentheses.

Not available in all fonts.
"""

STANDARD_SMALL = NoteheadTable(
    "noteheadDoubleWholeSmall",
    "noteheadWholeSmall",
    "noteheadHalfSmall",
    "noteheadBlackSmall",
)
"""Standard noteheads at a smaller size.

Not available in all fonts.
"""

STANDARD_OVERSIZED = NoteheadTable(
    "noteheadDoubleWholeOversized",
    "noteheadWholeOversized",
    "noteheadHalfOversized",
    "noteheadBlackOversized",
)
"""Standard noteheads at a larger size.

Not available in all fonts.
"""

X = NoteheadTable(
    "noteheadXDoubleWhole", "noteheadXWhole", "noteheadXHalf", "noteheadXBlack"
)
""""""

SLASH = NoteheadTable(
    "noteheadSlashWhiteDoubleWhole",
    "noteheadSlashWhiteWhole",
    "noteheadSlashWhiteHalf",
    "noteheadSlashVerticalEnds",
)
"""Percussion-style slash noteheads.

This uses SMuFL's vertical-ends-style short notehead.
"""

MUTED_SLASH = NoteheadTable(
    "noteheadSlashWhiteDoubleWhole",
    "noteheadSlashWhiteMuted",
    "noteheadSlashWhiteMuted",
    "noteheadSlashVerticalEndsMuted",
)
"""Percussion-style slash noteheads with secondary slashes indicating mutes.

Because SMuFL provides no muted variant for double whole notes, this
uses the regular slash double whole notehead.
"""

SLASH_OVERSIZED = NoteheadTable(
    "noteheadSlashWhiteDoubleWholeOversized",
    "noteheadSlashWhiteWholeOversized",
    "noteheadSlashWhiteHalfOversized",
    "noteheadSlashVerticalEndsOversized",
)
"""Like ``SLASH`` but with oversized variants.

Not available in all fonts.
"""

MUTED_SLASH_OVERSIZED = NoteheadTable(
    "noteheadSlashWhiteDoubleWholeOversized",
    "noteheadSlashWhiteMutedOversized",
    "noteheadSlashWhiteMutedOversized",
    "noteheadSlashVerticalEndsMutedOversized",
)
"""Like ``MUTED_SLASH`` but with oversized variants.

Not available in all fonts.
"""

PLUS = NoteheadTable(
    "noteheadPlusDoubleWhole",
    "noteheadPlusWhole",
    "noteheadPlusHalf",
    "noteheadPlusBlack",
)
""""""

CIRCLE_X = NoteheadTable(
    "noteheadCircleXDoubleWhole",
    "noteheadCircleXWhole",
    "noteheadCircleXHalf",
    "noteheadCircleX",
)
""""""

STANDARD_WITH_X = NoteheadTable(
    "noteheadDoubleWholeWithX",
    "noteheadWholeWithX",
    "noteheadHalfWithX",
    "noteheadVoidWithX",
)
""""""

SQUARE = NoteheadTable(
    "noteheadSquareWhite",
    "noteheadSquareWhite",
    "noteheadSquareWhite",
    "noteheadSquareBlack",
)
""""""

TRIANGLE_UP = NoteheadTable(
    "noteheadTriangleUpDoubleWhole",
    "noteheadTriangleUpWhole",
    "noteheadTriangleUpHalf",
    "noteheadTriangleUpBlack",
)
""""""

TRIANGLE_LEFT = NoteheadTable(
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftWhite",
    "noteheadTriangleLeftBlack",
)
""""""

TRIANGLE_RIGHT = NoteheadTable(
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightWhite",
    "noteheadTriangleRightBlack",
)
""""""

TRIANGLE_DOWN = NoteheadTable(
    "noteheadTriangleDownDoubleWhole",
    "noteheadTriangleDownWhole",
    "noteheadTriangleDownHalf",
    "noteheadTriangleDownBlack",
)
""""""

TRIANGLE_UP_RIGHT = NoteheadTable(
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightWhite",
    "noteheadTriangleUpRightBlack",
)
""""""

TRIANGLE_ROUND_DOWN = NoteheadTable(
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownWhite",
    "noteheadTriangleRoundDownBlack",
)
""""""

MOON = NoteheadTable(
    "noteheadMoonWhite",
    "noteheadMoonWhite",
    "noteheadMoonWhite",
    "noteheadMoonBlack",
)
""""""

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
""""""

DIAMOND_WIDE = NoteheadTable(
    "noteheadDiamondDoubleWhole",
    "noteheadDiamondWhole",
    "noteheadDiamondHalfWide",
    "noteheadDiamondBlackWide",
)
"""Like ``DIAMOND`` but with wider half and short variants"""

DIAMOND_OLD = NoteheadTable(
    "noteheadDiamondDoubleWholeOld",
    "noteheadDiamondWholeOld",
    "noteheadDiamondHalfOld",
    "noteheadDiamondBlackOld",
)
""""""

STANDARD_CIRCLED = NoteheadTable(
    "noteheadCircledDoubleWhole",
    "noteheadCircledWhole",
    "noteheadCircledHalf",
    "noteheadCircledBlack",
)
""""""

STANDARD_LARGE_CIRCLED = NoteheadTable(
    "noteheadCircledDoubleWholeLarge",
    "noteheadCircledWholeLarge",
    "noteheadCircledHalfLarge",
    "noteheadCircledBlackLarge",
)
"""Like ``STANDARD_CIRCLED`` but with a larger circle"""

LARGE_ARROW_UP = NoteheadTable(
    "noteheadLargeArrowUpDoubleWhole",
    "noteheadLargeArrowUpWhole",
    "noteheadLargeArrowUpHalf",
    "noteheadLargeArrowUpBlack",
)
""""""

LARGE_ARROW_DOWN = NoteheadTable(
    "noteheadLargeArrowDownDoubleWhole",
    "noteheadLargeArrowDownWhole",
    "noteheadLargeArrowDownHalf",
    "noteheadLargeArrowDownBlack",
)
""""""

CLUSTER_SQUARE = NoteheadTable(
    "noteheadClusterSquareWhite",
    "noteheadClusterSquareWhite",
    "noteheadClusterSquareWhite",
    "noteheadClusterSquareBlack",
)
"""Large tone clusters in square shapes

This uses the same glyph for all durations except ``short``.
"""

CLUSTER_ROUND = NoteheadTable(
    "noteheadClusterRoundWhite",
    "noteheadClusterRoundWhite",
    "noteheadClusterRoundWhite",
    "noteheadClusterRoundBlack",
)
"""Large tone clusters in round shapes

This uses the same glyph for all durations except ``short``.
"""

CLUSTER_SECOND = NoteheadTable(
    "noteheadClusterDoubleWhole2nd",
    "noteheadClusterWhole2nd",
    "noteheadClusterHalf2nd",
    "noteheadClusterQuarter2nd",
)
"""Tone cluster glyphs spanning a second"""

CLUSTER_THIRD = NoteheadTable(
    "noteheadClusterDoubleWhole3rd",
    "noteheadClusterWhole3rd",
    "noteheadClusterHalf3rd",
    "noteheadClusterQuarter3rd",
)
"""Tone cluster glyphs spanning a third"""

CLUSTER_SECOND_DIAMOND = NoteheadTable(
    "noteheadDiamondClusterWhite2nd",
    "noteheadDiamondClusterWhite2nd",
    "noteheadDiamondClusterWhite2nd",
    "noteheadDiamondClusterBlack2nd",
)
"""Tone cluster glyphs spanning a second using diamond glyphs

This uses the same glyph for all durations except ``short``.
"""

CLUSTER_THIRD_DIAMOND = NoteheadTable(
    "noteheadDiamondClusterWhite3rd",
    "noteheadDiamondClusterWhite3rd",
    "noteheadDiamondClusterWhite3rd",
    "noteheadDiamondClusterBlack3rd",
)
"""Tone cluster glyphs spanning a second using diamond glyphs

This uses the same glyph for all durations except ``short``.
"""

INVISIBLE = NoteheadTable("", "", "", "")
"""Blank non-printing noteheads"""

ALL_TABLES: List[NoteheadTable] = [
    STANDARD,
    STANDARD_WITH_PARENTHESES,
    STANDARD_SMALL,
    STANDARD_OVERSIZED,
    X,
    SLASH,
    MUTED_SLASH,
    SLASH_OVERSIZED,
    MUTED_SLASH_OVERSIZED,
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
    CLUSTER_SQUARE,
    CLUSTER_ROUND,
    CLUSTER_SECOND,
    CLUSTER_THIRD,
    CLUSTER_SECOND_DIAMOND,
    CLUSTER_THIRD_DIAMOND,
    INVISIBLE,
]
"""A list of all the notehead tables in this module

:meta hide-value:
"""
