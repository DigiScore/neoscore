import unittest

from brown.core import brown
from brown.core.beam import Beam
from brown.core.flowable_frame import FlowableFrame
from brown.core.staff import Staff
from brown.utils.parent_point import ParentPoint
from brown.core.path_element_type import PathElementType
from brown.core.path_element import PathElement
from brown.utils.point import Point
from brown.utils.units import Unit, Mm

from tests.mocks.mock_staff_object import MockStaffObject


class TestBeam(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.frame)
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_init_with_parent_point_args(self):
        beam = Beam(ParentPoint(Mm(1), Mm(2), self.left_parent),
                    ParentPoint(Mm(3), Mm(4), self.right_parent))
        assert(beam.parent == self.left_parent)
        assert(beam.pos == Point(Mm(1), Mm(2)))

    def test_init_with_tuple_args(self):
        beam = Beam((Mm(1), Mm(2), self.left_parent),
                    (Mm(3), Mm(4), self.right_parent))
        assert(beam.parent == self.left_parent)
        assert(beam.pos == Point(Mm(1), Mm(2)))

    def test_shape(self):
        beam = Beam(ParentPoint(Mm(1), Mm(2), self.left_parent),
                    ParentPoint(Mm(3), Mm(4), self.right_parent))
        thickness = beam.beam_thickness
        assert(len(beam.elements) == 5)
        PathElement._assert_soft_equal(
            beam.elements[0],
            PathElement(Point(Mm(0), Mm(0)),
                        PathElementType.move_to,
                        beam,
                        beam))
        PathElement._assert_soft_equal(
            beam.elements[1],
            PathElement(Point(Mm(3), Mm(4)),
                        PathElementType.line_to,
                        beam,
                        self.right_parent))
        PathElement._assert_soft_equal(
            beam.elements[2],
            PathElement(Point(Mm(3), Mm(4) + thickness),
                        PathElementType.line_to,
                        beam,
                        self.right_parent))
        PathElement._assert_soft_equal(
            beam.elements[3],
            PathElement(Point(Mm(0), thickness),
                        PathElementType.line_to,
                        beam,
                        beam))
        PathElement._assert_soft_equal(
            beam.elements[4],
            PathElement(Point(Mm(0), Mm(0)),
                        PathElementType.move_to,
                        beam,
                        beam))
