from neoscore.western.beam_group import BeamHook, BeamSpec, BeamState, resolve_beams


def test_resolve_beams():
    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(1)]) == [
        BeamState(3, hook=BeamHook.RIGHT),
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(3), BeamSpec(2)]) == [
        BeamState(1),
        BeamState(3, hook=BeamHook.RIGHT),
        BeamState(2),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(2), BeamSpec(1)]) == [
        BeamState(1),
        BeamState(2, hook=BeamHook.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(2), BeamSpec(3), BeamSpec(1)]) == [
        BeamState(2),
        BeamState(3, hook=BeamHook.LEFT),
        BeamState(1),
    ]

    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(3)]) == [
        BeamState(3, hook=BeamHook.RIGHT),
        BeamState(2),
        BeamState(3, hook=BeamHook.LEFT),
    ]

    assert resolve_beams([BeamSpec(1), BeamSpec(2), BeamSpec(3)]) == [
        BeamState(1),
        BeamState(2),
        BeamState(3, hook=BeamHook.LEFT),
    ]

    assert resolve_beams([BeamSpec(3), BeamSpec(2), BeamSpec(2)]) == [
        BeamState(3, hook=BeamHook.RIGHT),
        BeamState(2),
        BeamState(2),
    ]


def test_resolve_beams_with_hook_hints():
    assert resolve_beams(
        [BeamSpec(2), BeamSpec(2, hook=BeamHook.LEFT), BeamSpec(1)]
    ) == [
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(2),
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamSpec(2, hook=BeamHook.RIGHT), BeamSpec(2), BeamSpec(1)]
    ) == [
        BeamState(2),
        BeamState(2),  # Invalid hook hint is ignored
        BeamState(1),
    ]

    assert resolve_beams(
        [BeamSpec(1), BeamSpec(2, hook=BeamHook.RIGHT), BeamSpec(1)]
    ) == [
        BeamState(1),
        BeamState(2, hook=BeamHook.RIGHT),
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
        BeamState(3, None, BeamHook.RIGHT),
        BeamState(2),
    ]
