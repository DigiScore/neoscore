import unittest

from neoscore.core.directions import DirectionX, DirectionY
from neoscore.core.units import Unit


class TestDirectionY(unittest.TestCase):
    def test_direction_y_flip(self):
        assert DirectionY.DOWN.flip() == DirectionY.UP
        assert DirectionY.UP.flip() == DirectionY.DOWN

    def test_direction_y_from_sign(self):
        assert DirectionY.from_sign(-2) == DirectionY.UP
        assert DirectionY.from_sign(1) == DirectionY.DOWN
        assert DirectionY.from_sign(0) == DirectionY.DOWN
        assert DirectionY.from_sign(Unit(-1)) == DirectionY.UP
        assert DirectionY.from_sign(Unit(1)) == DirectionY.DOWN


class TestDirectionX(unittest.TestCase):
    def test_direction_x_flip(self):
        assert DirectionX.RIGHT.flip() == DirectionX.LEFT
        assert DirectionX.LEFT.flip() == DirectionX.RIGHT

    def test_direction_x_from_sign(self):
        assert DirectionX.from_sign(-2) == DirectionX.LEFT
        assert DirectionX.from_sign(1) == DirectionX.RIGHT
        assert DirectionX.from_sign(0) == DirectionX.RIGHT
        assert DirectionX.from_sign(Unit(-1)) == DirectionX.LEFT
        assert DirectionX.from_sign(Unit(1)) == DirectionX.RIGHT
