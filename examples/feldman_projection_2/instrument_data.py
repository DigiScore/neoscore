from typing import NamedTuple

from examples.feldman_projection_2.grid_unit import GridUnit
from examples.feldman_projection_2.measure import Measure
from examples.feldman_projection_2.register import Register
from neoscore.core.units import Unit


class EventData(NamedTuple):
    instrument: str
    pos_x: Unit
    register: Register
    text: str
    length: Unit


class InstrumentData:
    def __init__(self, name: str, event_data):
        self.name: str = name
        self.event_data = event_data
        self.occupied_measures: set[int] = self.calculate_occupied_measures(
            self.event_data
        )

    def measure_has_events(self, measure_number):
        return measure_number in self.occupied_measures

    @staticmethod
    def calculate_occupied_measures(event_data):
        occupied_measures = set()
        for event in event_data:
            start_measure_num = int(Measure(event.pos_x).display_value)
            end_measure_num = int(
                Measure(
                    event.pos_x + GridUnit(event.length) - GridUnit(1)
                ).display_value
            )
            occupied_measures.update(range(start_measure_num, end_measure_num + 1))
        return occupied_measures
