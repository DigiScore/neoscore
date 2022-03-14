from neoscore.utils.rect import Rect, rect_from_def
from neoscore.utils.units import Mm


def test_rect_multiplication():
    assert Rect(Mm(2), Mm(3), Mm(4), Mm(5)) * 2 == Rect(Mm(4), Mm(6), Mm(8), Mm(10))


def test_rect_from_def():
    args = (Mm(2), Mm(3), Mm(4), Mm(5))
    rect = Rect(*args)
    assert rect_from_def(rect) == rect
    assert rect_from_def(args) == rect
