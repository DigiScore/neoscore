from neoscore.core.flowable import Flowable
from neoscore.utils.units import Mm, Unit
from neoscore.western.slur import Slur
from neoscore.western.staff import Staff
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest


class TestSlur(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(5000))
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_doesnt_crash(self):
        """A woefully inadequate test to just see if slurs can be drawn at all.

        TODO LOW: Replace this with real tests
        """
        slur = Slur((Mm(1), Mm(2)), self.left_parent, (Mm(3), Mm(4)), self.right_parent)
