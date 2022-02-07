from brown.utils.units import Inch, Unit


class Measure(Unit):
    CONVERSION_RATE = Inch.CONVERSION_RATE / 2
