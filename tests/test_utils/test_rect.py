from brown.utils.rect import Rect
from brown.utils.units import Mm


def test_rect_in_unit():
    rect = Rect(1, 2, 99, 100)
    converted = rect.in_unit(Mm)
    assert converted.x == Mm(1)
    assert converted.y == Mm(2)
    assert converted.width == Mm(99)
    assert converted.height == Mm(100)


def test_rect_pos():
    rect = Rect(Mm(1), Mm(2), Mm(99), Mm(100))
    pos = rect.pos
    assert pos.x == Mm(1)
    assert pos.y == Mm(2)
