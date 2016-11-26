from nose.tools import assert_raises

from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import GraphicUnit


def test_rect_init():
    rect = Rect(1, 2, 99, 100)
    assert(rect.x == 1)
    assert(rect.y == 2)
    assert(rect.width == 99)
    assert(rect.height == 100)


def test_rect_with_unit():
    rect = Rect.with_unit(1, 2, 99, 100, GraphicUnit)
    assert(isinstance(rect.x, GraphicUnit))
    assert(rect.x == GraphicUnit(1))
    assert(isinstance(rect.y, GraphicUnit))
    assert(rect.y == GraphicUnit(2))
    assert(isinstance(rect.width, GraphicUnit))
    assert(rect.width == GraphicUnit(99))
    assert(isinstance(rect.height, GraphicUnit))
    assert(rect.height == GraphicUnit(100))
