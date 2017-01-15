from abc import ABC


class TimeLocation(ABC):

    """A logical time position with an unambiguous mapping to a point in time.

    This is an abstract class providing a common interface for time locations
    in different time schemes (e.g. metered durations, proportional durations,
    user-defined durations.)
    """

    def __init__(self):
        raise NotImplementedError
