from neoscore.core.flowable import Flowable
from neoscore.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.slur import Slur
from neoscore.western.staff import Staff
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest, assert_path_els_equal


class TestSlur(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable(ORIGIN, None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff(ORIGIN, self.flowable, Mm(5000))
        self.left_parent = MockStaffObject(ORIGIN, self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_path_elements(self):
        slur = Slur((Mm(1), Mm(2)), self.left_parent, (Mm(3), Mm(4)), self.right_parent)
        unit = self.staff.unit
        assert_path_els_equal(
            slur.elements,
            [
                MoveTo(Point(unit(0.0), unit(-0.1)), slur),
                CurveTo(
                    Point(Mm(3), Mm(3.825)),
                    self.right_parent,
                    ControlPoint(Point(ZERO, unit(-0.97)), slur),
                    ControlPoint(Point(Mm(3), Mm(2.302)), self.right_parent),
                ),
                LineTo(Point(Mm(3), Mm(4)), self.right_parent),
                CurveTo(
                    ORIGIN,
                    slur,
                    ControlPoint(Point(Mm(3), Mm(2.688)), self.right_parent),
                    ControlPoint(Point(ZERO, unit(-0.75)), slur),
                ),
            ],
            epsilon=0.5,
        )
