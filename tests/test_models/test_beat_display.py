import pytest

from neoscore.models.beat_display import BaseDuration, BeatDisplay


def test_base_duration_validation():
    BaseDuration(0)
    BaseDuration(1)
    BaseDuration(2)
    BaseDuration(4)
    BaseDuration(8)
    BaseDuration(16)
    BaseDuration(32)
    BaseDuration(2**20)
    with pytest.raises(ValueError):
        BaseDuration(-2)
        BaseDuration(-1)
        BaseDuration(3)
        BaseDuration(5)


def test_beat_display_flag_count():
    assert BeatDisplay(BaseDuration(0), 0).flag_count == 0
    assert BeatDisplay(BaseDuration(1), 0).flag_count == 0
    assert BeatDisplay(BaseDuration(2), 0).flag_count == 0
    assert BeatDisplay(BaseDuration(4), 0).flag_count == 0
    assert BeatDisplay(BaseDuration(8), 0).flag_count == 1
    assert BeatDisplay(BaseDuration(16), 0).flag_count == 2
    assert BeatDisplay(BaseDuration(32), 0).flag_count == 3
    assert BeatDisplay(BaseDuration(64), 0).flag_count == 4
    assert BeatDisplay(BaseDuration(2**20), 0).flag_count == 18
