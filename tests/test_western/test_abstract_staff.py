from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.paper import Paper
from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.staff_group import StaffGroup
from tests.helpers import assert_almost_equal

from ..helpers import AppTest


class TestTabStaff(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.document.paper = Paper(
            *[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        )
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))
        self.font = MusicFont("Bravura", Mm(1))

    def test_staff_group(self):
        staff = AbstractStaff(ORIGIN, None, Mm(100), None, Mm(1), 5, self.font, None)
        assert staff.group is not None
        group = StaffGroup()
        staff = AbstractStaff(ORIGIN, None, Mm(100), group, Mm(1), 5, self.font, None)
        assert staff.group == group

    def test_height(self):
        # 5 lines
        assert_almost_equal(
            AbstractStaff(
                (Mm(0), Mm(0)),
                self.flowable,
                Mm(100),
                None,
                Mm(1.5),
                5,
                self.font,
                None,
            ).height,
            Mm(6),
        )
        assert_almost_equal(
            AbstractStaff(
                (Mm(0), Mm(0)), self.flowable, Mm(100), None, Mm(1), 5, self.font, None
            ).height,
            Mm(4),
        )
        # 4 lines
        assert_almost_equal(
            AbstractStaff(
                (Mm(0), Mm(0)),
                self.flowable,
                Mm(100),
                None,
                Mm(1.5),
                4,
                self.font,
                None,
            ).height,
            Mm(4.5),
        )
        assert_almost_equal(
            AbstractStaff(
                (Mm(0), Mm(0)), self.flowable, Mm(100), None, Mm(1), 4, self.font, None
            ).height,
            Mm(3),
        )

    def test_center_y(self):
        staff = AbstractStaff(ORIGIN, None, Mm(100), None, Mm(1), 3, self.font, None)
        assert staff.center_y == Mm(1)

    def test_barline_extent_multi_line(self):
        staff = AbstractStaff(ORIGIN, None, Mm(100), None, Mm(1), 4, self.font, None)
        assert staff.barline_extent == (ZERO, staff.unit(3))

    def test_barline_extent_single_line(self):
        staff = AbstractStaff(ORIGIN, None, Mm(100), None, Mm(1), 1, self.font, None)
        assert staff.barline_extent == (staff.unit(-1), staff.unit(1))

    def test_y_inside_staff_with_odd_line_count(self):
        staff = AbstractStaff(
            (Mm(0), Mm(0)), self.flowable, Mm(100), None, Mm(1), 5, self.font, None
        )
        assert staff.y_inside_staff(staff.unit(0)) is True
        assert staff.y_inside_staff(staff.unit(4)) is True
        assert staff.y_inside_staff(staff.unit(5)) is False
        assert staff.y_inside_staff(staff.unit(-5)) is False

    def test_y_inside_staff_with_even_line_count(self):
        staff = AbstractStaff(
            (Mm(0), Mm(0)), self.flowable, Mm(100), None, Mm(1), 4, self.font, None
        )
        assert staff.y_inside_staff(staff.unit(0)) is True
        assert staff.y_inside_staff(staff.unit(3)) is True
        assert staff.y_inside_staff(staff.unit(4)) is False
        assert staff.y_inside_staff(staff.unit(-4)) is False
