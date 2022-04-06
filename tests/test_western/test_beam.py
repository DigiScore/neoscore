from neoscore.core.flowable import Flowable
from neoscore.core.path_element import LineTo, MoveTo
from neoscore.core.point import Point
from neoscore.core.units import Mm, Unit
from neoscore.western.beam import Beam
from neoscore.western.staff import Staff
from tests.helpers import assert_path_els_equal
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest


class TestBeam(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(5000))
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_init_with_parent_point_args(self):
        beam = Beam((Mm(1), Mm(2)), self.left_parent, (Mm(3), Mm(4)), self.right_parent)
        assert beam.parent == self.left_parent
        assert beam.pos.x == Mm(1)
        assert beam.pos.y == Mm(2)

    def test_init_with_tuple_args(self):
        beam = Beam((Mm(1), Mm(2)), self.left_parent, (Mm(3), Mm(4)), self.right_parent)
        assert beam.parent == self.left_parent
        assert beam.pos.x == Mm(1)
        assert beam.pos.y == Mm(2)

    def test_shape(self):
        beam = Beam((Mm(1), Mm(2)), self.left_parent, (Mm(3), Mm(4)), self.right_parent)
        thickness = beam.beam_thickness
        assert len(beam.elements) == 5
        assert_path_els_equal(beam.elements[0], MoveTo(Point(Mm(0), Mm(0)), beam))
        assert_path_els_equal(
            beam.elements[1], LineTo(Point(Mm(3), Mm(4)), self.right_parent)
        )
        assert_path_els_equal(
            beam.elements[2],
            LineTo(
                Point(Mm(3), Mm(4) + thickness),
                self.right_parent,
            ),
        )
        assert_path_els_equal(
            beam.elements[3],
            LineTo(
                Point(Mm(0), thickness),
                beam,
            ),
        )
        assert_path_els_equal(
            beam.elements[4],
            LineTo(
                Point(Mm(0), Mm(0)),
                beam,
            ),
        )
