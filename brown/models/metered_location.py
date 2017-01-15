from brown.models.time_location import TimeLocation
from brown.models.duration import Duration


class MeteredLocation(TimeLocation):

    """A logical time position in metered time.

    This consists of a measure number and a Duration within that measure.
    """

    def __init__(self, measure_number, offset=None):
        """
        Args:
            measure_number (int): The measure number
            offset (Duration): The offset within the bar
        """
        self.measure_number = measure_number
        if offset:
            self.offset = offset
        else:
            self.offset = Duration(0, 1)
