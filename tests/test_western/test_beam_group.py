from neoscore.core.directions import DirectionX, DirectionY
from neoscore.core.point import Point
from neoscore.core.units import Mm

# noinspection PyProtectedMember
from neoscore.western.beam_group import (
    BeamGroup,
    _BeamGroupLine,
    _BeamPathSpec,
    _BeamState,
    _resolve_beam_direction,
    _resolve_beam_group_height,
    _resolve_beam_group_line,
    _resolve_beam_hooks,
    _resolve_beam_layout,
)
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

from ..helpers import AppTest, assert_almost_equal


def test_resolve_beam_hooks():
    assert _resolve_beam_hooks([_BeamState(3), _BeamState(2), _BeamState(1)]) == [
        _BeamState(3, hook=DirectionX.RIGHT),
        _BeamState(2),
        _BeamState(1),
    ]

    assert _resolve_beam_hooks([_BeamState(1), _BeamState(3), _BeamState(2)]) == [
        _BeamState(1),
        _BeamState(3, hook=DirectionX.RIGHT),
        _BeamState(2),
    ]

    assert _resolve_beam_hooks([_BeamState(1), _BeamState(2), _BeamState(1)]) == [
        _BeamState(1),
        _BeamState(2, hook=DirectionX.LEFT),
        _BeamState(1),
    ]

    assert _resolve_beam_hooks([_BeamState(2), _BeamState(3), _BeamState(1)]) == [
        _BeamState(2),
        _BeamState(3, hook=DirectionX.LEFT),
        _BeamState(1),
    ]

    assert _resolve_beam_hooks([_BeamState(3), _BeamState(2), _BeamState(3)]) == [
        _BeamState(3, hook=DirectionX.RIGHT),
        _BeamState(2),
        _BeamState(3, hook=DirectionX.LEFT),
    ]

    assert _resolve_beam_hooks([_BeamState(1), _BeamState(2), _BeamState(3)]) == [
        _BeamState(1),
        _BeamState(2),
        _BeamState(3, hook=DirectionX.LEFT),
    ]

    assert _resolve_beam_hooks([_BeamState(3), _BeamState(2), _BeamState(2)]) == [
        _BeamState(3, hook=DirectionX.RIGHT),
        _BeamState(2),
        _BeamState(2),
    ]


def test_resolve_beam_hooks_with_break_depth():
    assert _resolve_beam_hooks(
        [_BeamState(1), _BeamState(2, 1), _BeamState(3), _BeamState(3)]
    ) == [
        _BeamState(1),
        _BeamState(2, 1, DirectionX.LEFT),
        _BeamState(3),
        _BeamState(3),
    ]


def test_resolve_beam_hooks_with_hook_hints():
    assert _resolve_beam_hooks(
        [_BeamState(2), _BeamState(2, hook=DirectionX.LEFT), _BeamState(1)]
    ) == [
        _BeamState(2),  # Invalid hook hint is ignored
        _BeamState(2),
        _BeamState(1),
    ]

    assert _resolve_beam_hooks(
        [_BeamState(2, hook=DirectionX.RIGHT), _BeamState(2), _BeamState(1)]
    ) == [
        _BeamState(2),
        _BeamState(2),  # Invalid hook hint is ignored
        _BeamState(1),
    ]

    assert _resolve_beam_hooks(
        [_BeamState(1), _BeamState(2, hook=DirectionX.RIGHT), _BeamState(1)]
    ) == [
        _BeamState(1),
        _BeamState(2, hook=DirectionX.RIGHT),
        _BeamState(1),
    ]


def test_resolve_beam_hooks_break_depths_copied():
    assert _resolve_beam_hooks([_BeamState(3), _BeamState(3, 1), _BeamState(3)]) == [
        _BeamState(3),
        _BeamState(3, 1),
        _BeamState(3),
    ]
    assert _resolve_beam_hooks([_BeamState(3, 2), _BeamState(3, 1), _BeamState(3)]) == [
        _BeamState(3, 2),
        _BeamState(3, 1),
        _BeamState(3),
    ]
    assert _resolve_beam_hooks([_BeamState(3), _BeamState(3), _BeamState(3, 1)]) == [
        _BeamState(3),
        _BeamState(3),
        _BeamState(3, 1),
    ]


def test_resolve_beam_hooks_with_break_depths_affecting_flags():
    assert _resolve_beam_hooks(
        [_BeamState(2), _BeamState(2, 1), _BeamState(3), _BeamState(2)]
    ) == [
        _BeamState(2),
        _BeamState(2, 1),
        _BeamState(3, None, DirectionX.RIGHT),
        _BeamState(2),
    ]


def test_resolve_beam_layout():
    # Simplest case of 2 8th notes
    assert _resolve_beam_layout([_BeamState(1), _BeamState(1)]) == [
        _BeamPathSpec(1, 0, 1),
    ]

    # 2 16th notes
    assert _resolve_beam_layout([_BeamState(2), _BeamState(2)]) == [
        _BeamPathSpec(1, 0, 1),
        _BeamPathSpec(2, 0, 1),
    ]

    # Several 64th notes
    assert _resolve_beam_layout([_BeamState(4)] * 10) == [
        _BeamPathSpec(1, 0, 9),
        _BeamPathSpec(2, 0, 9),
        _BeamPathSpec(3, 0, 9),
        _BeamPathSpec(4, 0, 9),
    ]

    # 32nd notes with 2 groups of 16ths
    assert _resolve_beam_layout(
        [_BeamState(3), _BeamState(3, 1), _BeamState(3), _BeamState(3)]
    ) == [
        _BeamPathSpec(1, 0, 3),
        _BeamPathSpec(2, 0, 1),
        _BeamPathSpec(2, 2, 3),
        _BeamPathSpec(3, 0, 1),
        _BeamPathSpec(3, 2, 3),
    ]

    # Starting and ending hooks
    assert _resolve_beam_layout(
        [
            _BeamState(3, hook=DirectionX.RIGHT),
            _BeamState(2),
            _BeamState(3, hook=DirectionX.LEFT),
        ]
    ) == [
        _BeamPathSpec(1, 0, 2),
        _BeamPathSpec(2, 0, 2),
        _BeamPathSpec(3, 0, DirectionX.RIGHT),
        _BeamPathSpec(3, 2, DirectionX.LEFT),
    ]

    # Subgroups and a hook
    assert _resolve_beam_layout(
        [
            _BeamState(2),
            _BeamState(2, 1),
            _BeamState(3, None, DirectionX.RIGHT),
            _BeamState(2),
        ]
    ) == [
        _BeamPathSpec(1, 0, 3),
        _BeamPathSpec(2, 0, 1),
        _BeamPathSpec(2, 2, 3),
        _BeamPathSpec(3, 2, DirectionX.RIGHT),
    ]


class TestResolveBeamDirection(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        Clef(Mm(0), self.staff, "treble")

    def test_resolve_beam_direction_with_single_notes(self):
        assert (
            _resolve_beam_direction(
                [
                    Chordrest(Mm(1), self.staff, ["c,,,"], (1, 8)),
                    Chordrest(Mm(10), self.staff, ["f"], (1, 8)),
                ]
            )
            == DirectionY.UP
        )

    def test_resolve_beam_direction_with_chords_only_uses_furthest(self):
        assert (
            _resolve_beam_direction(
                [
                    Chordrest(Mm(1), self.staff, ["c,,,", "c", "c", "c", "c"], (1, 8)),
                    Chordrest(Mm(10), self.staff, ["f", "e", "e", "e"], (1, 8)),
                ]
            )
            == DirectionY.UP
        )

    def test_resolve_beam_direction_with_rests(self):
        assert (
            _resolve_beam_direction(
                [
                    Chordrest(Mm(10), self.staff, ["c'"], (1, 8)),
                    Chordrest(Mm(10), self.staff, [], (1, 8)),
                ]
            )
            == DirectionY.DOWN
        )

    def test_resolve_beam_direction_at_center_goes_down(self):
        assert (
            _resolve_beam_direction(
                [
                    Chordrest(Mm(10), self.staff, [], (1, 8)),
                    Chordrest(Mm(10), self.staff, ["b"], (1, 8)),
                ]
            )
            == DirectionY.DOWN
        )


class TestResolveBeamGroupHeight(AppTest):
    def test_resolve_beam_group_height(self):
        staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        font = staff.music_font
        Clef(Mm(0), staff, "treble")

        layer_height = (
            font.engraving_defaults["beamSpacing"]
            + font.engraving_defaults["beamThickness"]
        )

        def cr(numerator, denominator):
            return Chordrest(Mm(1), staff, ["c,"], (numerator, denominator))

        assert _resolve_beam_group_height([cr(1, 8), cr(1, 8)], font) == layer_height
        assert (
            _resolve_beam_group_height([cr(1, 16), cr(1, 8)], font) == layer_height * 2
        )
        assert _resolve_beam_group_height([cr(3, 16)], font) == layer_height
        assert (
            _resolve_beam_group_height([cr(3, 16), cr(1, 16)], font) == layer_height * 2
        )


class TestResolveBeamGroupLine(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        self.font = self.staff.music_font
        self.unit = self.font.unit
        self.beam_layer_height = (
            self.font.engraving_defaults["beamSpacing"]
            + self.font.engraving_defaults["beamThickness"]
        )
        Clef(Mm(0), self.staff, "treble")

    def assert_lines_eq(self, left: _BeamGroupLine, right: _BeamGroupLine):
        assert_almost_equal(left.start_y, right.start_y, places=1)
        self.assertAlmostEqual(left.slope, right.slope)

    def test_beam_group_line_flat_above(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g"], (1, 8)),
        ]
        assert _resolve_beam_group_line(
            crs, DirectionY.UP, self.font
        ) == _BeamGroupLine(
            crs[0].highest_notehead.y - self.unit(2.5) - self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_below(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g"], (1, 8)),
        ]
        assert _resolve_beam_group_line(
            crs, DirectionY.DOWN, self.font
        ) == _BeamGroupLine(
            crs[0].lowest_notehead.y + self.unit(2.5) + self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_above_with_higher_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["f", "c'"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["g"], (1, 8)),
        ]
        assert _resolve_beam_group_line(
            crs, DirectionY.UP, self.font
        ) == _BeamGroupLine(
            crs[1].highest_notehead.y - self.unit(2.5) - self.beam_layer_height, 0
        )

    def test_beam_group_line_flat_below_with_many_beams(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 32)),
            Chordrest(Mm(20), self.staff, ["g"], (1, 64)),
        ]
        assert _resolve_beam_group_line(
            crs, DirectionY.DOWN, self.font
        ) == _BeamGroupLine(
            crs[0].lowest_notehead.y + self.unit(2.5) + self.beam_layer_height * 4, 0
        )

    def test_beam_group_line_slanted_upward(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["a"], (1, 8)),
        ]
        self.assert_lines_eq(
            _resolve_beam_group_line(crs, DirectionY.UP, self.font),
            _BeamGroupLine(Mm(-3.063), 0.175),
        )

    def test_beam_group_line_slanted_upward_with_closer_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["g"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["f'"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["a"], (1, 8)),
        ]
        self.assert_lines_eq(
            _resolve_beam_group_line(crs, DirectionY.UP, self.font),
            _BeamGroupLine(Mm(-6.562), 0.0875),
        )

    def test_beam_group_line_slanted_downward(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["a"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g"], (1, 8)),
        ]
        self.assert_lines_eq(
            _resolve_beam_group_line(crs, DirectionY.DOWN, self.font),
            _BeamGroupLine(Mm(12.688), -0.175),
        )

    def test_beam_group_line_slanted_downward_with_closer_notes(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["a"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["b", "c,,"], (1, 8)),
            Chordrest(Mm(30), self.staff, ["g"], (1, 8)),
        ]
        self.assert_lines_eq(
            _resolve_beam_group_line(crs, DirectionY.DOWN, self.font),
            _BeamGroupLine(Mm(27.562), -0.0875),
        )


class TestBeamGroup(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(Point(Mm(0), Mm(0)), None, Mm(100))
        Clef(Mm(0), self.staff, "treble")

    def test_beam_direction_override(self):
        crs = [
            Chordrest(Mm(10), self.staff, ["a"], (1, 8)),
            Chordrest(Mm(20), self.staff, ["g"], (1, 8)),
        ]
        bg = BeamGroup(crs)
        assert bg.direction == DirectionY.UP
        bg = BeamGroup(crs, DirectionY.DOWN)
        assert bg.direction == DirectionY.DOWN
