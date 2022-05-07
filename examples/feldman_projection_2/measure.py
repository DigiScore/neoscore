from neoscore.core.units import Inch, Unit


class Measure(Unit):
    """The length of a measure, which in this piece is constant length."""

    CONVERSION_RATE = Inch.CONVERSION_RATE * 0.8
