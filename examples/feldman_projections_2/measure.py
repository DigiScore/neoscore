from examples.feldman_projections_2.grid_unit import GridUnit
from brown.utils.units import Unit


class Measure(Unit):
    CONVERSION_RATE = GridUnit.CONVERSION_RATE * 4
