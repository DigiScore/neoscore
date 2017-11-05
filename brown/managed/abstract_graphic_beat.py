from brown.models.beat import Beat
from brown.utils.units import Unit


class AbstractGraphicBeat(Beat, Unit):

    """A GraphicBeat without defined Unit conversion attributes.

    This is meant to be subclassed by class factory methods in
    context managers. Factory methods only need to define
    `CONVERSION_RATE` and `_constant_offset` to implement a
    concrete graphic beat.

    This should never be instantiated directly.

    NOTE: This was hackily extracted from an older version of Beat,
          and it doesn't work.
    """
    # Rate of a 1/1 beat to GraphicUnit(1)
    CONVERSION_RATE = None
    # A constant offset to be applied to all unit conversions.
    _constant_offset = 0

    def __init__(self, *args):
        """
        *args:
            numerator (int or Beat):
            denominator (int):
        OR:
            float_value (float): A floating point number to be
                approximated into a quantized beat.
        OR:
            beat (Beat): An existing Beat
        """
        # Can (probably?) skip unit init entirely
        # Unit.__init__(self, 0)  # Placeholder 0 in unit init?
        Beat.__init__(self, *args)

    ######## CONSTRUCTORS ########

    @classmethod
    def from_unit(cls, unit):
        float_value = ((unit._to_base_unit_float()
                        - cls._constant_offset)
                       / cls.CONVERSION_RATE)
        return cls(float_value)

    ######## PRIVATE METHODS ########

    def _to_base_unit_float(self):
        """Return this value as a float in base unit values.

        Returns: float
        """
        if self._constant_offset:
            return ((self.value * self.CONVERSION_RATE)
                    + Unit(self._constant_offset).value)
        else:
            return self.value * self.CONVERSION_RATE

    @classmethod
    def make_concrete_beat(cls,
                           whole_note_size,
                           constant_offset=None,
                           name=None):
        """Make a concrete GraphicBeat class and return it.

        Args:
            whole_note_size (Unit): The length of a Beat(1, 1)
            constant_offset (Unit): A constant offset for all conversions.
            name (str): The name for the concrete Beat class.
                If not specified, 'ConcreteBeat' is used.

        Returns: type
        """
        class GraphicBeat(cls):
            CONVERSION_RATE = Unit(whole_note_size).value
            _constant_offset = (Unit(constant_offset).value if constant_offset
                                else 0)

        if name:
            GraphicBeat.__name__ = name
        return GraphicBeat
