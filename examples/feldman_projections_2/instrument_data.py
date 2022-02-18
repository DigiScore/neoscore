from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.measure import Measure


class InstrumentData:
    def __init__(self, name, event_data):
        self.name = name
        self.event_data = event_data
        self.occupied_measures = self.calculate_occupied_measures(self.event_data)

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
