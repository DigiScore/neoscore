from neoscore.core.units import Inch, Unit


class Measure(Unit):
    CONVERSION_RATE = Inch.CONVERSION_RATE * 0.8
