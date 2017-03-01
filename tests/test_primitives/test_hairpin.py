import unittest

from brown.core import brown
from brown.utils.units import Unit, Mm
from brown.utils.anchored_point import AnchoredPoint
from brown.primitives.hairpin import Hairpin
from brown.core.flowable_frame import FlowableFrame
from brown.primitives.staff import Staff

from mock_staff_object import MockStaffObject


class TestHairpin(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.frame)
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_find_hairpin_points_horizontal_same_parent(self):
        cresc = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                        (Unit(10), Unit(0), 0, self.left_parent),
                        1,
                        Unit(2))
        points = cresc._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(10), Unit(1), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(0), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(10), Unit(-1), parent=self.left_parent))

        dim = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                      (Unit(10), Unit(0), 0, self.left_parent),
                      -1,
                      Unit(2))
        points = dim._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(0), Unit(1), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(10), Unit(0), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(0), Unit(-1), parent=self.left_parent))

    def test_find_hairpin_points_horizontal_different_parent(self):
        cresc = Hairpin((Unit(0), Unit(2), 0, self.left_parent),
                        (Unit(1), Unit(0), 0, self.right_parent),
                        1,
                        Unit(2))
        points = cresc._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(1), Unit(1), parent=self.right_parent))
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(2), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(1), Unit(-1), parent=self.right_parent))

        dim = Hairpin((Unit(0), Unit(2), 0, self.left_parent),
                      (Unit(1), Unit(0), 0, self.right_parent),
                      -1,
                      Unit(2))
        points = dim._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(0), Unit(3), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(1), Unit(0), parent=self.right_parent))
        assert(points[2] == AnchoredPoint(
            Unit(0), Unit(1), parent=self.left_parent))

    def test_find_hairpin_points_vertical_same_parent(self):
        cresc = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                        (Unit(0), Unit(10), 0, self.left_parent),
                        1,
                        Unit(2))
        points = cresc._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(1), Unit(10), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(0), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(-1), Unit(10), parent=self.left_parent))

        dim = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                      (Unit(0), Unit(10), 0, self.left_parent),
                      -1,
                      Unit(2))
        points = dim._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(1), Unit(0), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(10), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(-1), Unit(0), parent=self.left_parent))

    def test_find_hairpin_points_vertical_different_parents(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                        (Unit(-10), Unit(1), 0, self.right_parent),
                        1,
                        Unit(2))
        points = cresc._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(-9), Unit(1), parent=self.right_parent))
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(0), parent=self.left_parent))
        assert(points[2] == AnchoredPoint(
            Unit(-11), Unit(1), parent=self.right_parent))

        dim = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                      (Unit(-10), Unit(1), 0, self.right_parent),
                      -1,
                      Unit(2))
        points = dim._find_hairpin_points()
        assert(points[0] == AnchoredPoint(
            Unit(1), Unit(0), parent=self.left_parent))
        assert(points[1] == AnchoredPoint(
            Unit(-10), Unit(1), parent=self.right_parent))
        assert(points[2] == AnchoredPoint(
            Unit(-1), Unit(0), parent=self.left_parent))

    def test_hairpin_points_diagonal_same_parent(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                        (Unit(4), Unit(4), 0, self.left_parent),
                        1,
                        Unit(2))
        # Spanner line slope should be Unit(1)
        points = cresc._find_hairpin_points()
        self.assertAlmostEqual(Unit(points[0].x).value,
                               Unit(points[2].y).value)
        self.assertAlmostEqual(Unit(points[0].y).value,
                               Unit(points[2].x).value)
        assert(points[1] == AnchoredPoint(
            Unit(0), Unit(0), parent=self.left_parent))

        dim = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                      (Unit(4), Unit(4), 0, self.left_parent),
                      -1,
                      Unit(2))
        # Spanner line slope should be Unit(1)
        points = dim._find_hairpin_points()
        self.assertAlmostEqual(Unit(points[0].x).value,
                               Unit(points[2].y).value)
        self.assertAlmostEqual(Unit(points[0].y).value,
                               Unit(points[2].x).value)
        assert(points[1] == AnchoredPoint(Unit(4), Unit(4),
                                          parent=self.left_parent))

    def test_hairpin_points_diagonal_different_parents(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin((Unit(10), Unit(2), 0, self.left_parent),
                        (Unit(4), Unit(4), 0, self.right_parent),
                        1,
                        Unit(2))
        # Spanner line slope should be Unit(1)
        points = cresc._find_hairpin_points()
        self.assertAlmostEqual(Unit(points[0].x).value,
                               Unit(points[2].y).value)
        self.assertAlmostEqual(Unit(points[0].y).value,
                               Unit(points[2].x).value)
        assert(points[1] == AnchoredPoint(
            Unit(10), Unit(2), parent=self.left_parent))

        dim = Hairpin((Unit(0), Unit(0), 0, self.left_parent),
                      (Unit(-6), Unit(2), 0, self.right_parent),
                      -1,
                      Unit(2))
        # Spanner line slope should be Unit(1)
        points = dim._find_hairpin_points()
        self.assertAlmostEqual(Unit(points[0].x).value,
                               Unit(points[2].y).value)
        self.assertAlmostEqual(Unit(points[0].y).value,
                               Unit(points[2].x).value)
        assert(points[1] == AnchoredPoint(
            Unit(-6), Unit(2), parent=self.right_parent))
