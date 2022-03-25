import pytest

from neoscore.models.beat_display import BeatDisplay


def test_base_duration_validation():
    BeatDisplay(0, 0)
    BeatDisplay(1, 0)
    BeatDisplay(2, 0)
    BeatDisplay(4, 0)
    BeatDisplay(8, 0)
    BeatDisplay(16, 0)
    BeatDisplay(32, 0)
    BeatDisplay(2**20, 0)
    with pytest.raises(ValueError):
        BeatDisplay(-2, 0)
    with pytest.raises(ValueError):
        BeatDisplay(-1, 0)
    with pytest.raises(ValueError):
        BeatDisplay(3, 0)
    with pytest.raises(ValueError):
        BeatDisplay(5, 0)


def test_beat_display_flag_count():
    assert BeatDisplay(0, 0).flag_count == 0
    assert BeatDisplay(1, 0).flag_count == 0
    assert BeatDisplay(2, 0).flag_count == 0
    assert BeatDisplay(4, 0).flag_count == 0
    assert BeatDisplay(8, 0).flag_count == 1
    assert BeatDisplay(16, 0).flag_count == 2
    assert BeatDisplay(32, 0).flag_count == 3
    assert BeatDisplay(64, 0).flag_count == 4
    assert BeatDisplay(2**20, 0).flag_count == 18


def test_beat_display_requires_stem():
    assert BeatDisplay(256, 0).requires_stem is True
    assert BeatDisplay(64, 0).requires_stem is True
    assert BeatDisplay(4, 0).requires_stem is True
    assert BeatDisplay(2, 0).requires_stem is True
    assert BeatDisplay(1, 0).requires_stem is False
    assert BeatDisplay(0, 0).requires_stem is False
