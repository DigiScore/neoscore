import unittest

from brown.core import brown
from brown.core.beam import Beam
from brown.core.flowable import Flowable
from brown.core.path_element import LineTo, MoveTo
from brown.core.staff import Staff
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point
from brown.utils.units import Mm, Unit
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import assert_path_els_equal


class TestBeam(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.flowable)
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_init_with_parent_point_args(self):
        beam = Beam(
            ParentPoint(Mm(1), Mm(2), self.left_parent),
            ParentPoint(Mm(3), Mm(4), self.right_parent),
        )
        assert beam.parent == self.left_parent
        assert beam.pos.x == Mm(1)
        assert beam.pos.y == Mm(2)

    def test_init_with_tuple_args(self):
        beam = Beam((Mm(1), Mm(2), self.left_parent), (Mm(3), Mm(4), self.right_parent))
        assert beam.parent == self.left_parent
        assert beam.pos.x == Mm(1)
        assert beam.pos.y == Mm(2)

    def test_shape(self):
        beam = Beam(
            ParentPoint(Mm(1), Mm(2), self.left_parent),
            ParentPoint(Mm(3), Mm(4), self.right_parent),
        )
        thickness = beam.beam_thickness
        assert len(beam.elements) == 4
        assert_path_els_equal(
            beam.elements[0], LineTo(Point(Mm(3), Mm(4)), self.right_parent)
        )
        assert_path_els_equal(
            beam.elements[1],
            LineTo(
                Point(Mm(3), Mm(4) + thickness),
                self.right_parent,
            ),
        )
        assert_path_els_equal(
            beam.elements[2],
            LineTo(
                Point(Mm(0), thickness),
                beam,
            ),
        )
        assert_path_els_equal(
            beam.elements[3],
            MoveTo(
                Point(Mm(0), Mm(0)),
                beam,
            ),
        )
