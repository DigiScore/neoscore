from neoscore.core.flowable import Flowable
from neoscore.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.staff import Staff
from neoscore.western.tie import Tie
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest, assert_path_els_equal


class TestTie(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable(ORIGIN, None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff(ORIGIN, self.flowable, Mm(5000))
        self.left_parent = MockStaffObject(ORIGIN, self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_path_elements(self):
        tie = Tie((Mm(1), Mm(2)), self.left_parent, Mm(3), self.right_parent)
        unit = self.staff.unit
        assert_path_els_equal(
            tie.elements,
            [
                MoveTo(Point(ZERO, unit(-0.1)), tie),
                CurveTo(
                    Point(Mm(3), Mm(1.119)),
                    self.right_parent,
                    ControlPoint(Point(ZERO, unit(-0.97)), tie),
                    ControlPoint(Point(Mm(3), Mm(-0.403)), self.right_parent),
                ),
                LineTo(Point(Mm(3), Mm(1.294)), self.right_parent),
                CurveTo(
                    ORIGIN,
                    tie,
                    ControlPoint(Point(Mm(3), Mm(-0.018)), self.right_parent),
                    ControlPoint(Point(ZERO, unit(-0.75)), tie),
                ),
            ],
            epsilon=0.5,
        )
