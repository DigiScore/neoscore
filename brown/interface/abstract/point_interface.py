from abc import ABC

# This is probably not going to be needed - too much bloat

class PointInterface(ABC):
    """A 2-d point."""
    def __init__(self, x, y):
        """
        Args:
            x (float): x-axis position
            y (float): y-axis position
        """
        raise NotImplementedError
