import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.staff import Staff
from brown.models.beat import Beat
from brown.core.clef import Clef
from brown.core.notehead import Notehead
from brown.utils.units import Mm


class TestNotehead(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(10000), flowable=self.flowable)
        Clef(self.staff, Mm(0), 'treble')

    def test_staff_position_middle_c_treble(self):
        self.assertEqual(Notehead(Mm(10), "c'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(5))

    def test_staff_position_low_octaves(self):
        self.assertEqual(Notehead(Mm(10), "c",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(8.5))
        self.assertEqual(Notehead(Mm(10), "c,",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(12))
        self.assertEqual(Notehead(Mm(10), "c,,",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(15.5))
        self.assertEqual(Notehead(Mm(10), "c,,,",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(19))

    def test_staff_position_high_octaves(self):
        self.assertEqual(Notehead(Mm(10), "c''",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(1.5))
        self.assertEqual(Notehead(Mm(10), "c'''",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(-2))
        self.assertEqual(Notehead(Mm(10), "c''''",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(-5.5))
        self.assertEqual(Notehead(Mm(10), "c'''''",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(-9))

    def test_staff_position_with_accidentals(self):
        self.assertEqual(Notehead(Mm(10), "cf'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(5))
        self.assertEqual(Notehead(Mm(10), "cn'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(5))
        self.assertEqual(Notehead(Mm(10), "cs'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(5))

    def test_staff_position_with_all_letter_names(self):
        self.assertEqual(Notehead(Mm(10), "d'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(4.5))
        self.assertEqual(Notehead(Mm(10), "e'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(4))
        self.assertEqual(Notehead(Mm(10), "f'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(3.5))
        self.assertEqual(Notehead(Mm(10), "g'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(3))
        self.assertEqual(Notehead(Mm(10), "a'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(2.5))
        self.assertEqual(Notehead(Mm(10), "b'",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(2))

    def test_staff_position_on_later_flowable_line(self):
        self.assertEqual(Notehead(Mm(1000), "c",
                                  Beat(1, 4),
                                  self.staff).staff_position,
                         self.staff.unit(8.5))
