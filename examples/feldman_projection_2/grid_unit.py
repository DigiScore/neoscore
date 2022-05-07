from examples.feldman_projection_2.measure import Measure
from neoscore.core.units import Unit


class GridUnit(Unit):
    """A unit representing a single grid square length"""

    CONVERSION_RATE = Measure.CONVERSION_RATE / 4
