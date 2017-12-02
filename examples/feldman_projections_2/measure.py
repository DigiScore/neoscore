from brown.utils.units import Unit, Inch


class Measure(Unit):
    CONVERSION_RATE = Inch.CONVERSION_RATE / 2
