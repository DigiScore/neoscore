from examples.feldman_projections_2.measure import Measure


class InstrumentData:

    def __init__(self, name, event_data):
        self.name = name
        self.event_data = event_data

    def measure_has_events(self, measure_number):
        return any(
            Measure(measure_number) <= e.pos_x <= Measure(measure_number + 1)
            for e in self.event_data
        )
