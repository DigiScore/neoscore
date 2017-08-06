import unittest

from brown.core import brown
from brown.utils.units import Unit
from brown.core.invisible_object import InvisibleObject
from brown.earle.move import Move


class TestMove(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.grob_1 = InvisibleObject((Unit(0), Unit(0)))
        self.grob_2 = InvisibleObject((Unit(10), Unit(10)))

    def test_move_one(self):
        move = Move([self.grob_1], Unit(5), Unit(6))
        move.execute()
        self.assertEqual(self.grob_1.x, Unit(5))
        self.assertEqual(self.grob_1.y, Unit(6))

        move.undo()
        self.assertEqual(self.grob_1.x, Unit(0))
        self.assertEqual(self.grob_1.y, Unit(0))

    def test_move_multiple(self):
        move = Move([self.grob_1, self.grob_2], Unit(5), Unit(6))
        move.execute()
        self.assertEqual(self.grob_1.x, Unit(5))
        self.assertEqual(self.grob_1.y, Unit(6))
        self.assertEqual(self.grob_2.x, Unit(15))
        self.assertEqual(self.grob_2.y, Unit(16))

        move.undo()
        self.assertEqual(self.grob_1.x, Unit(0))
        self.assertEqual(self.grob_1.y, Unit(0))
        self.assertEqual(self.grob_2.x, Unit(10))
        self.assertEqual(self.grob_2.y, Unit(10))
