import unittest

from examples.feldman_projections_2.content import EventData
from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.instrument_data import InstrumentData
from examples.feldman_projections_2.measure import Measure
from examples.feldman_projections_2.register import Register


class TestInstrumentData(unittest.TestCase):

    def test_calculate_occupied_measures_one_grid_unit_event(self):

        data = [EventData('', Measure(0) + GridUnit(3), Register.M, '', GridUnit(1))]

        assert(InstrumentData.calculate_occupied_measures(data) == {0})

