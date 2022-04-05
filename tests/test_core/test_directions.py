import unittest

from neoscore.core.directions import HorizontalDirection, VerticalDirection
from neoscore.utils.units import Unit


class TestVerticalDirection(unittest.TestCase):
    def test_vertical_direction_flip(self):
        assert VerticalDirection.DOWN.flip() == VerticalDirection.UP
        assert VerticalDirection.UP.flip() == VerticalDirection.DOWN

    def test_vertical_direction_from_sign(self):
        assert VerticalDirection.from_sign(-2) == VerticalDirection.UP
        assert VerticalDirection.from_sign(1) == VerticalDirection.DOWN
        assert VerticalDirection.from_sign(0) == VerticalDirection.DOWN
        assert VerticalDirection.from_sign(Unit(-1)) == VerticalDirection.UP
        assert VerticalDirection.from_sign(Unit(1)) == VerticalDirection.DOWN


class TestHorizontalDirection(unittest.TestCase):
    def test_horizontal_direction_flip(self):
        assert HorizontalDirection.RIGHT.flip() == HorizontalDirection.LEFT
        assert HorizontalDirection.LEFT.flip() == HorizontalDirection.RIGHT

    def test_horizontal_direction_from_sign(self):
        assert HorizontalDirection.from_sign(-2) == HorizontalDirection.LEFT
        assert HorizontalDirection.from_sign(1) == HorizontalDirection.RIGHT
        assert HorizontalDirection.from_sign(0) == HorizontalDirection.RIGHT
        assert HorizontalDirection.from_sign(Unit(-1)) == HorizontalDirection.LEFT
        assert HorizontalDirection.from_sign(Unit(1)) == HorizontalDirection.RIGHT
