from brown.models.interval import Interval


class Transposition:

    """A pitch transposition represented as an interval"""

    def __init__(self, interval):
        """
        Args:
            interval (Interval or str representation):
        """
        self.interval = (interval if isinstance(interval, Interval)
                         else Interval(interval))
