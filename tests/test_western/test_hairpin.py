from neoscore.core.directions import DirectionX
from neoscore.core.flowable import Flowable
from neoscore.core.point import Point
from neoscore.core.units import Mm, Unit
from neoscore.western.hairpin import Hairpin
from neoscore.western.staff import Staff
from tests.helpers import assert_almost_equal
from tests.mocks.mock_staff_object import MockStaffObject

from ..helpers import AppTest


class TestHairpin(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(5000))
        self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)

    def test_find_hairpin_points_horizontal_same_parent(self):
        cresc = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(10), Unit(0)),
            self.left_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        points = cresc._find_hairpin_points()
        assert points == (
            Point(Unit(10), Unit(1)),
            self.left_parent,
            Point(Unit(0), Unit(0)),
            self.left_parent,
            Point(Unit(10), Unit(-1)),
            self.left_parent,
        )

        dim = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(10), Unit(0)),
            self.left_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        points = dim._find_hairpin_points()
        assert points == (
            Point(Unit(0), Unit(1)),
            self.left_parent,
            Point(Unit(10), Unit(0)),
            self.left_parent,
            Point(Unit(0), Unit(-1)),
            self.left_parent,
        )

    def test_find_hairpin_points_horizontal_different_parent(self):
        cresc = Hairpin(
            (Unit(0), Unit(2)),
            self.left_parent,
            (Unit(1), Unit(0)),
            self.right_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        points = cresc._find_hairpin_points()
        assert points == (
            Point(Unit(1), Unit(1)),
            self.right_parent,
            Point(Unit(0), Unit(2)),
            self.left_parent,
            Point(Unit(1), Unit(-1)),
            self.right_parent,
        )

        dim = Hairpin(
            (Unit(0), Unit(2)),
            self.left_parent,
            (Unit(1), Unit(0)),
            self.right_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        points = dim._find_hairpin_points()
        assert points == (
            Point(Unit(0), Unit(3)),
            self.left_parent,
            Point(Unit(1), Unit(0)),
            self.right_parent,
            Point(Unit(0), Unit(1)),
            self.left_parent,
        )

    def test_find_hairpin_points_vertical_same_parent(self):
        cresc = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(0), Unit(10)),
            self.left_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        points = cresc._find_hairpin_points()
        assert points == (
            Point(Unit(1), Unit(10)),
            self.left_parent,
            Point(Unit(0), Unit(0)),
            self.left_parent,
            Point(Unit(-1), Unit(10)),
            self.left_parent,
        )

        dim = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(0), Unit(10)),
            self.left_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        points = dim._find_hairpin_points()
        assert points == (
            Point(Unit(1), Unit(0)),
            self.left_parent,
            Point(Unit(0), Unit(10)),
            self.left_parent,
            Point(Unit(-1), Unit(0)),
            self.left_parent,
        )

    def test_find_hairpin_points_vertical_different_parents(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(-10), Unit(1)),
            self.right_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        points = cresc._find_hairpin_points()
        assert points == (
            Point(Unit(-9), Unit(1)),
            self.right_parent,
            Point(Unit(0), Unit(0)),
            self.left_parent,
            Point(Unit(-11), Unit(1)),
            self.right_parent,
        )

        dim = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(-10), Unit(1)),
            self.right_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        points = dim._find_hairpin_points()
        assert points == (
            Point(Unit(1), Unit(0)),
            self.left_parent,
            Point(Unit(-10), Unit(1)),
            self.right_parent,
            Point(Unit(-1), Unit(0)),
            self.left_parent,
        )

    def test_hairpin_points_diagonal_same_parent(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(4), Unit(4)),
            self.left_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        # Spanner line slope should be Unit(1)
        points = cresc._find_hairpin_points()
        assert_almost_equal(points[0].x, points[4].y)
        assert_almost_equal(points[0].y, points[4].x)
        assert points[2] == Point(Unit(0), Unit(0))
        assert points[3] == self.left_parent

        dim = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(4), Unit(4)),
            self.left_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        # Spanner line slope should be Unit(1)
        points = dim._find_hairpin_points()
        assert_almost_equal(points[0].x, points[4].y)
        assert_almost_equal(points[0].y, points[4].x)
        assert points[2] == Point(Unit(4), Unit(4))
        assert points[3] == self.left_parent

    def test_hairpin_points_diagonal_different_parents(self):
        # For reference...
        # self.left_parent = MockStaffObject((Unit(0), Unit(0)), self.staff)
        # self.right_parent = MockStaffObject((Unit(10), Unit(2)), self.staff)
        cresc = Hairpin(
            (Unit(10), Unit(2)),
            self.left_parent,
            (Unit(4), Unit(4)),
            self.right_parent,
            DirectionX.RIGHT,
            Unit(2),
        )
        # Spanner line slope should be Unit(1)
        points = cresc._find_hairpin_points()
        assert_almost_equal(points[0].x, points[4].y)
        assert_almost_equal(points[0].y, points[4].x)
        assert points[2] == Point(Unit(10), Unit(2))
        assert points[3] == self.left_parent

        dim = Hairpin(
            (Unit(0), Unit(0)),
            self.left_parent,
            (Unit(-6), Unit(2)),
            self.right_parent,
            DirectionX.LEFT,
            Unit(2),
        )
        # Spanner line slope should be Unit(1)
        points = dim._find_hairpin_points()
        assert_almost_equal(points[0].x, points[4].y)
        assert_almost_equal(points[0].y, points[4].x)
        assert points[2] == Point(Unit(-6), Unit(2))
        assert points[3] == self.right_parent
