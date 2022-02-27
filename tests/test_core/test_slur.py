import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.slur import Slur
from brown.core.staff import Staff
from brown.utils.units import Mm, Unit
from tests.mocks.mock_staff_object import MockStaffObject


class TestSlur(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.flowable)
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def testDrawingDoesntCrash(self):
        """A woefully inadequate test to just see if slurs can be drawn at all.

        TODO LOW: Replace this with real tests
        """
        slur = Slur((Mm(1), Mm(2), self.left_parent), (Mm(3), Mm(4), self.right_parent))
