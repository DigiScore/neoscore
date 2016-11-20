import pytest

from brown.utils.point import Point
from brown.utils.rect import Rect


def test_rect_init_two_points():
    rect = Rect(Point(1, 2), Point(100, 102))
    assert(rect.x == 1)
    assert(rect.y == 2)
    assert(rect.width == 99)
    assert(rect.height == 100)

def test_rect_init_two_tuples():
    rect = Rect((1, 2), (100, 102))
    assert(rect.x == 1)
    assert(rect.y == 2)
    assert(rect.width == 99)
    assert(rect.height == 100)

def test_rect_init_four_positions():
    rect = Rect(1, 2, 99, 100)
    assert(rect.x == 1)
    assert(rect.y == 2)
    assert(rect.width == 99)
    assert(rect.height == 100)

def test_rect_init_invalid():
    with pytest.raises(TypeError):
        rect = Rect(1, 2, 99)
