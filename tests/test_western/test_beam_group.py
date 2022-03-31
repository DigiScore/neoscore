import unittest

from neoscore.core import neoscore
from neoscore.models.directions import HorizontalDirection, VerticalDirection
from neoscore.utils.point import Point
from neoscore.utils.units import Mm
from neoscore.western.beam_group import (
    BeamGroupLine,
    BeamPathSpec,
    BeamState,
    resolve_beam_direction,
    resolve_beam_group_height,
    resolve_beam_group_line,
    resolve_beam_layout,
    resolve_beams,
)
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

from ..helpers import assert_almost_equal


def test_resolve_beams():
    assert resolve_beams([BeamState(3), BeamState(2), BeamState(1)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams([BeamState(1), BeamState(3), BeamState(2)]) == [
        BeamState(1),
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
    ]

    assert resolve_beams([BeamState(1), BeamState(2), BeamState(1)]) == [
        BeamState(1),
        BeamState(2, hook=HorizontalDirection.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamState(2), BeamState(3), BeamState(1)]) == [
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamState(3), BeamState(2), BeamState(3)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
    ]

    assert resolve_beams([BeamState(1), BeamState(2), BeamState(3)]) == [
        BeamState(1),
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
    ]

    assert resolve_beams([BeamState(3), BeamState(2), BeamState(2)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(2),
    ]


def test_resolve_beams_with_hook_hints():
    assert resolve_beams(
        [BeamState(2), BeamState(2, hook=HorizontalDirection.LEFT), BeamState(1)]
    ) == [
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamState(2, hook=HorizontalDirection.RIGHT), BeamState(2), BeamState(1)]
    ) == [
        BeamState(2),
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamState(1), BeamState(2, hook=HorizontalDirection.RIGHT), BeamState(1)]
    ) == [
        BeamState(1),
        BeamState(2, hook=HorizontalDirection.RIGHT),
        BeamState(1),
    ]


def test_resolve_beams_break_depths_copied():
    assert resolve_beams([BeamState(3), BeamState(3, 1), BeamState(3)]) == [
        BeamState(3),
        BeamState(3, 1),
        BeamState(3),
    ]
    assert resolve_beams([BeamState(3, 2), BeamState(3, 1), BeamState(3)]) == [
        BeamState(3, 2),
        BeamState(3, 1),
        BeamState(3),
    ]
    assert resolve_beams([BeamState(3), BeamState(3), BeamState(3, 1)]) == [
        BeamState(3),
        BeamState(3),
        BeamState(3, 1),
    ]


def test_resolve_beams_with_break_depths_affecting_flags():
    assert resolve_beams(
        [BeamState(2), BeamState(2, 1), BeamState(3), BeamState(2)]
    ) == [
        BeamState(2),
        BeamState(2, 1),
        BeamState(3, None, HorizontalDirection.RIGHT),
        BeamState(2),
    ]


def test_resolve_beam_layout():
    # Simplest case of 2 8th notes
    assert resolve_beam_layout([BeamState(1), BeamState(1)]) == [
        BeamPathSpec(1, 0, 1),
    ]

    # 2 16th notes
    assert resolve_beam_layout([BeamState(2), BeamState(2)]) == [
        BeamPathSpec(1, 0, 1),
        BeamPathSpec(2, 0, 1),
    ]

    # Several 64th notes
    assert resolve_beam_layout([BeamState(4)] * 10) == [
        BeamPathSpec(1, 0, 9),
        BeamPathSpec(2, 0, 9),
        BeamPathSpec(3, 0, 9),
        BeamPathSpec(4, 0, 9),
    ]

    # 32nd notes with 2 groups of 16ths
    assert resolve_beam_layout(
        [BeamState(3), BeamState(3, 1), BeamState(3), BeamState(3)]
    ) == [
        BeamPathSpec(1, 0, 3),
        BeamPathSpec(2, 0, 1),
        BeamPathSpec(2, 2, 3),
        BeamPathSpec(3, 0, 1),
        BeamPathSpec(3, 2, 3),
    ]

    # Starting and ending hooks
    assert resolve_beam_layout(
        [
            BeamState(3, hook=HorizontalDirection.RIGHT),
            BeamState(2),
            BeamState(3, hook=HorizontalDirection.LEFT),
        ]
    ) == [
        BeamPathSpec(1, 0, 2),
        BeamPathSpec(2, 0, 2),
        BeamPathSpec(3, 0, HorizontalDirection.RIGHT),
        BeamPathSpec(3, 2, HorizontalDirection.LEFT),
    ]

    # Subgroups and a hook
    assert resolve_beam_layout(
        [
            BeamState(2),
            BeamState(2, 1),
            BeamState(3, None, HorizontalDirection.RIGHT),
            BeamState(2),
        ]
    ) == [
        BeamPathSpec(1, 0, 3),
        BeamPathSpec(2, 0, 1),
        BeamPathSpec(2, 2, 3),
        BeamPathSpec(3, 2, HorizontalDirection.RIGHT),
    ]


class TestResolveBeamDirection(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        Clef(Mm(0), self.staff, "treble")

    def test_resolve_beam_direction_with_single_notes(self):
        assert (
            resolve_beam_direction(
                [
                    Chordrest(Mm(1), self.staff, ["c,,"], (1, 8)),
                    Chordrest(Mm(10), self.staff, ["f'"], (1, 8)),
                ]
            )
            == VerticalDirection.UP
        )

    def test_resolve_beam_direction_with_chords_only_uses_furthest(self):
        assert (
            resolve_beam_direction(
                [
                    Chordrest(
                        Mm(1), self.staff, ["c,,", "c'", "c'", "c'", "c'"], (1, 8)
                    ),
                    Chordrest(Mm(10), self.staff, ["f'", "e'", "e'", "e'"], (1, 8)),
                ]
            )
            == VerticalDirection.UP
        )

    def test_resolve_beam_direction_with_rests(self):
        assert (
            resolve_beam_direction(
                [
                    Chordrest(Mm(10), self.staff, ["c''"], (1, 8)),
                    Chordrest(Mm(10), self.staff, [], (1, 8)),
                ]
            )
            == VerticalDirection.DOWN
        )

    def test_resolve_beam_direction_at_center_goes_down(self):
        assert (
            resolve_beam_direction(
                [
                    Chordrest(Mm(10), self.staff, [], (1, 8)),
                    Chordrest(Mm(10), self.staff, ["b'"], (1, 8)),
                ]
            )
            == VerticalDirection.DOWN
        )


def test_resolve_beam_group_height():
    neoscore.setup()
    staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
    font = staff.music_font
    Clef(Mm(0), staff, "treble")

    layer_height = (
        font.engraving_defaults["beamSpacing"]
        + font.engraving_defaults["beamThickness"]
    )

    def cr(numerator, denominator):
        return Chordrest(Mm(1), staff, ["c"], (numerator, denominator))

    assert resolve_beam_group_height([cr(1, 8), cr(1, 8)], font) == layer_height
    assert resolve_beam_group_height([cr(1, 16), cr(1, 8)], font) == layer_height * 2
    assert resolve_beam_group_height([cr(3, 16)], font) == layer_height
    assert resolve_beam_group_height([cr(3, 16), cr(1, 16)], font) == layer_height * 2


class TestResolveBeamGroupLine(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        self.font = self.staff.music_font
        self.unit = self.font.unit
        self.beam_layer_height = (
            self.font.engraving_defaults["beamSpacing"]
            + self.font.engraving_defaults["beamThickness"]
        )
        Clef(Mm(0), self.staff, "treble")

    def assert_lines_eq(self, left: BeamGroupLine, right: BeamGroupLine):
        assert_almost_equal(left.start_y, right.start_y)
        self.assertAlmostEqual(left.slope, right.slope)

    def test_beam_group_line_flat_above(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g'"], (1, 8)),
        ]
        assert resolve_beam_group_line(
            crs, VerticalDirection.UP, self.font
        ) == BeamGroupLine(
            crs[0].highest_notehead.y - self.unit(3.5) - self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_below(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g'"], (1, 8)),
        ]
        assert resolve_beam_group_line(
            crs, VerticalDirection.DOWN, self.font
        ) == BeamGroupLine(
            crs[0].lowest_notehead.y + self.unit(3.5) + self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_above_with_higher_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["f'", "c''"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["g'"], (1, 8)),
        ]
        assert resolve_beam_group_line(
            crs, VerticalDirection.UP, self.font
        ) == BeamGroupLine(
            crs[1].highest_notehead.y - self.unit(3.5) - self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_below_with_many_beams(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 32)),
            Chordrest(Mm(20), self.staff, ["g'"], (1, 64)),
        ]
        assert resolve_beam_group_line(
            crs, VerticalDirection.DOWN, self.font
        ) == BeamGroupLine(
            crs[0].lowest_notehead.y + self.unit(3.5) + self.beam_layer_height * 4, 0
        )

    def test_beam_group_line_slanted_upward(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["a'"], (1, 8)),
        ]
        self.assert_lines_eq(
            resolve_beam_group_line(crs, VerticalDirection.UP, self.font),
            BeamGroupLine(Mm(-2.75), 0.0999999999),
        )

    def test_beam_group_line_slanted_upward_with_closer_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["f''"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["a'"], (1, 8)),
        ]
        self.assert_lines_eq(
            resolve_beam_group_line(crs, VerticalDirection.UP, self.font),
            BeamGroupLine(Mm(-4.75), 0.049999999),
        )

    def test_beam_group_line_slanted_downward(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["a'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g'"], (1, 8)),
        ]
        self.assert_lines_eq(
            resolve_beam_group_line(crs, VerticalDirection.DOWN, self.font),
            BeamGroupLine(Mm(8.25), -0.0999999999),
        )

    def test_beam_group_line_slanted_downward_with_closer_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["a'"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["b'", "c,"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["g'"], (1, 8)),
        ]
        self.assert_lines_eq(
            resolve_beam_group_line(crs, VerticalDirection.DOWN, self.font),
            BeamGroupLine(Mm(16.75), -0.04999999),
        )
