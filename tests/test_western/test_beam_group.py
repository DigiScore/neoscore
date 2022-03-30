from neoscore.models.directions import HorizontalDirection
from neoscore.western.beam_group import (
    BeamPathSpec,
    BeamSpec,
    BeamState,
    resolve_beam_layout,
    resolve_beams,
)


def test_resolve_beams():
    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(1)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(3), BeamSpec(2)]) == [
        BeamState(1),
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(2), BeamSpec(1)]) == [
        BeamState(1),
        BeamState(2, hook=HorizontalDirection.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(2), BeamSpec(3), BeamSpec(1)]) == [
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(3)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(2), BeamSpec(3)]) == [
        BeamState(1),
        BeamState(2),
        BeamState(3, hook=HorizontalDirection.LEFT),
    ]

    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(2)]) == [
        BeamState(3, hook=HorizontalDirection.RIGHT),
        BeamState(2),
        BeamState(2),
    ]


def test_resolve_beams_with_hook_hints():
    assert resolve_beams(
        [BeamSpec(2), BeamSpec(2, hook=HorizontalDirection.LEFT), BeamSpec(1)]
    ) == [
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamSpec(2, hook=HorizontalDirection.RIGHT), BeamSpec(2), BeamSpec(1)]
    ) == [
        BeamState(2),
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamSpec(1), BeamSpec(2, hook=HorizontalDirection.RIGHT), BeamSpec(1)]
    ) == [
        BeamState(1),
        BeamState(2, hook=HorizontalDirection.RIGHT),
        BeamState(1),
    ]


def test_resolve_beams_break_depths_copied():
    assert resolve_beams([BeamSpec(3), BeamSpec(3, 1), BeamSpec(3)]) == [
        BeamState(3),
        BeamState(3, 1),
        BeamState(3),
    ]
    assert resolve_beams([BeamSpec(3, 2), BeamSpec(3, 1), BeamSpec(3)]) == [
        BeamState(3, 2),
        BeamState(3, 1),
        BeamState(3),
    ]
    assert resolve_beams([BeamSpec(3), BeamSpec(3), BeamSpec(3, 1)]) == [
        BeamState(3),
        BeamState(3),
        BeamState(3, 1),
    ]


def test_resolve_beams_with_break_depths_affecting_flags():
    assert resolve_beams([BeamSpec(2), BeamSpec(2, 1), BeamSpec(3), BeamSpec(2)]) == [
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
