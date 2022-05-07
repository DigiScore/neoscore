from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Mm


def test_rect_multiplication():
    assert Rect(Mm(2), Mm(3), Mm(4), Mm(5)) * 2 == Rect(Mm(4), Mm(6), Mm(8), Mm(10))


def test_rect_from_def():
    args = (Mm(2), Mm(3), Mm(4), Mm(5))
    rect = Rect(*args)
    assert Rect.from_def(rect) == rect
    assert Rect.from_def(args) == rect


def test_rect_offset():
    assert Rect(Mm(2), Mm(3), Mm(10), Mm(20)).offset(Point(Mm(1), Mm(1))) == Rect(
        Mm(3), Mm(4), Mm(10), Mm(20)
    )


def test_rect_merge():
    r1 = Rect(Mm(2), Mm(-10), Mm(1), Mm(30))
    r2 = Rect(Mm(-5), Mm(10), Mm(15), Mm(2))
    assert r1.merge(r2) == Rect(Mm(-5), Mm(-10), Mm(15), Mm(30))
