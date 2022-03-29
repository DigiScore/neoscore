from neoscore.models.duration_display import DurationDisplay
from neoscore.western.beam_group import BeamHook, BeamState, resolve_beams


def make_durs(flag_counts: list[int]):
    return [DurationDisplay(2 ** (count + 2), 0) for count in flag_counts]


def test_resolve_beams():
    assert resolve_beams(make_durs([3, 2, 1])) == [
        BeamState(3, BeamHook.RIGHT),
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams(make_durs([2, 3, 1])) == [
        BeamState(2),
        BeamState(3, BeamHook.LEFT),
        BeamState(1),
    ]

    assert resolve_beams(make_durs([3, 2, 3])) == [
        BeamState(3, BeamHook.RIGHT),
        BeamState(2),
        BeamState(3, BeamHook.LEFT),
    ]

    assert resolve_beams(make_durs([1, 2, 3])) == [
        BeamState(1),
        BeamState(2),
        BeamState(3, BeamHook.LEFT),
    ]

    assert resolve_beams(make_durs([3, 2, 2])) == [
        BeamState(3, BeamHook.RIGHT),
        BeamState(2),
        BeamState(2),
    ]
