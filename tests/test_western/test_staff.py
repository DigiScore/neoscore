import pytest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.paper import Paper
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Mm
from neoscore.western import clef_type
from neoscore.western.clef import Clef
from neoscore.western.staff import NoClefError, Staff
from tests.helpers import assert_almost_equal

from ..helpers import AppTest


class TestStaff(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.document.paper = Paper(
            *[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        )
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))

    def test_allows_pen_override(self):
        pen = Pen("#ff0000")
        staff = Staff(ORIGIN, self.flowable, Mm(100), pen=pen)
        assert staff.pen == pen

    def test_default_pen_thickness_matches_smufl(self):
        staff = Staff(ORIGIN, self.flowable, Mm(100))
        assert (
            staff.pen.thickness
            == staff.music_font.engraving_defaults["staffLineThickness"]
        )

    def test_distance_to_next_of_type(self):
        staff = Staff((Mm(10), Mm(0)), self.flowable, Mm(100))
        treble = Clef(Mm(11), staff, "treble")
        bass = Clef(Mm(31), staff, "bass")
        assert_almost_equal(staff.distance_to_next_of_type(treble), Mm(20))
        assert_almost_equal(staff.distance_to_next_of_type(bass), Mm(100 - 31))

    def test_active_clef_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), staff, "treble")
        Clef(Mm(10), staff, "bass")
        # Test between two clefs should have treble in effect
        assert staff.active_clef_at(Mm(1)).clef_type == clef_type.TREBLE
        # Test after bass clef goes into effect
        assert staff.active_clef_at(Mm(11)).clef_type == clef_type.BASS

    def test_active_clef_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        assert staff.active_clef_at(Mm(5)) is None

    def test_middle_c_at_with_explicit_clefs(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), staff, "treble")
        Clef(Mm(10), staff, "bass")
        # Test between two clefs should be in treble mode
        assert staff.middle_c_at(Mm(1)) == staff.unit(5)
        # Test after bass clef goes into effect
        assert staff.middle_c_at(Mm(11)) == staff.unit(-1)

    def test_middle_c_at_with_implicit_default_clef(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100))
        with pytest.raises(NoClefError):
            staff.middle_c_at(Mm(5))

    def test_position_on_ledger_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=5)
        assert staff.y_on_ledger(staff.unit(-1)) is True
        assert staff.y_on_ledger(staff.unit(-0.5)) is False
        assert staff.y_on_ledger(staff.unit(0)) is False
        assert staff.y_on_ledger(staff.unit(4)) is False
        assert staff.y_on_ledger(staff.unit(4.5)) is False
        assert staff.y_on_ledger(staff.unit(5)) is True

    def test_ledgers_needed_from_position_with_odd_line_count(self):
        staff = Staff((Mm(0), Mm(0)), self.flowable, Mm(100), line_count=5)
        # Inside the staff, no ledgers
        assert staff.ledgers_needed_for_y(staff.unit(0)) == []
        assert staff.ledgers_needed_for_y(staff.unit(4)) == []
        # Just outside the staff, no ledgers
        assert staff.ledgers_needed_for_y(staff.unit(-0.5)) == []
        assert staff.ledgers_needed_for_y(staff.unit(4.5)) == []
        # Right on the first ledger
        assert staff.ledgers_needed_for_y(staff.unit(-1)) == [staff.unit(-1)]
        assert staff.ledgers_needed_for_y(staff.unit(5)) == [staff.unit(5)]
        # Further outside with multiple ledgers, directly on lines
        assert staff.ledgers_needed_for_y(staff.unit(6)) == [
            staff.unit(6),
            staff.unit(5),
        ]
        assert staff.ledgers_needed_for_y(staff.unit(-2)) == [
            staff.unit(-2),
            staff.unit(-1),
        ]
        # Further outside with multiple ledgers, between lines
        assert staff.ledgers_needed_for_y(staff.unit(6.5)) == [
            staff.unit(6),
            staff.unit(5),
        ]
        assert staff.ledgers_needed_for_y(staff.unit(-2.5)) == [
            staff.unit(-2),
            staff.unit(-1),
        ]

    def test_path_drawing(self):
        staff = Staff((Mm(2), Mm(3)), self.flowable, Mm(10), None, Mm(1))
        path = staff._create_staff_segment_path(Point(Mm(2), Mm(3)), Mm(10))
        self.flowable.render()
        # Top line
        assert path.elements[0].pos == Point(Mm(0), Mm(0))
        assert path.elements[0].parent == path
        assert path.elements[1].pos == Point(Mm(10), Mm(0))
        assert path.elements[1].parent == path
        # Second line
        assert path.elements[2].pos == Point(Mm(0), Mm(1))
        assert path.elements[2].parent == path
        assert path.elements[3].pos == Point(Mm(10), Mm(1))
        assert path.elements[3].parent == path
