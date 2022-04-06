import pytest

from neoscore.western.duration_display import DurationDisplay


def test_base_duration_validation():
    DurationDisplay(0, 0)
    DurationDisplay(1, 0)
    DurationDisplay(2, 0)
    DurationDisplay(4, 0)
    DurationDisplay(8, 0)
    DurationDisplay(16, 0)
    DurationDisplay(32, 0)
    DurationDisplay(2**20, 0)
    with pytest.raises(ValueError):
        DurationDisplay(-2, 0)
    with pytest.raises(ValueError):
        DurationDisplay(-1, 0)
    with pytest.raises(ValueError):
        DurationDisplay(3, 0)
    with pytest.raises(ValueError):
        DurationDisplay(5, 0)


def test_duration_display_flag_count():
    assert DurationDisplay(0, 0).flag_count == 0
    assert DurationDisplay(1, 0).flag_count == 0
    assert DurationDisplay(2, 0).flag_count == 0
    assert DurationDisplay(4, 0).flag_count == 0
    assert DurationDisplay(8, 0).flag_count == 1
    assert DurationDisplay(16, 0).flag_count == 2
    assert DurationDisplay(32, 0).flag_count == 3
    assert DurationDisplay(64, 0).flag_count == 4
    assert DurationDisplay(2**20, 0).flag_count == 18


def test_duration_display_requires_stem():
    assert DurationDisplay(256, 0).requires_stem is True
    assert DurationDisplay(64, 0).requires_stem is True
    assert DurationDisplay(4, 0).requires_stem is True
    assert DurationDisplay(2, 0).requires_stem is True
    assert DurationDisplay(1, 0).requires_stem is False
    assert DurationDisplay(0, 0).requires_stem is False
