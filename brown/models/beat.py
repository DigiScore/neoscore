from fractions import Fraction
from warnings import warn

from brown.utils.units import Unit


class AbstractBeatConversionError(Exception):
    """Exception raised when an abstract Beat is converted to a concrete unit.

    Beats can only be converted to other (graphical) units when they have a
    defined _conversion_rate.
    """
    def __init__(self):
        self.message = ('Cannot convert an abstract Beat to a concrete Unit. '
                        'To work with Beats in a graphical context, '
                        'a concrete Beat type should be created with '
                        'Beat.make_concrete_beat()')
        super().__init__(self.message)


class Beat(Unit):
    """A beat in a meter whose value is measured in rational numbers.

    The beat fraction indicates beat as a fraction of a whole note.
    The actual written denomination of beat is deduced
    from the reduced fraction. For instance:

    * `Beat(1, 4)` indicates a quarter note value
    * `Beat(1, 1)` indicates a whole note value
    * `Beat(3, 8)` indicates a dotted quarter note value

    Arbitrarily nested tuplets can be created by nesting Beats
    in each other. To do this, let the numerator of a Beat
    be a Beat where the denominator indicates the division
    within the outer Beat. The actual written denomination
    of the durataion is inferred.

    * `Beat(Beat(1, 3), 4)` indicates an eighth in a triplet
      spanning a quarter
    * `Beat(Beat(1, 5), 8)` indicates a 32nd in a quintuplet
      spanning an eighth
    * `Beat(Beat(2, 10), 8)` is equivalent to
      `Beat(Beat(1, 5), 8)` seen above, for the same reason
      that `Beat(2, 8)` is equivalent to `Beat(1, 4)`
    * `Beat(Beat(3, 10), 8)` indicates a dotted 32nd in a quintuplet
      spanning an eighth.

    Nested Beats are not reduced into each other:
    * `Beat(Beat(1, 2), 4)` is *not* equivalent to `Beat(1, 8)`

    Beats should be treated as immutable, and will not work correctly
    if their properties are changed after initialization.

    # TODO: How to handle things like duplet over dotted quarter?
    """

    # unit conversion rate in default Beat is uninitialized.
    # Users should generally not create Beats directly - they should
    # work with beats through staves, whose layout systems will create
    # local Beat classes which implement this conversion rate
    _conversion_rate = None
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

        **kwargs:

        """
        if self._conversion_rate is None:
            warn('Initializing an abstract Beat. '
                 'You probably don\'t want to be doing this.')
        if len(args) == 2:
            self._numerator, self._denominator = args
        elif len(args) == 1:
            if isinstance(args[0], type(self)):
                self._numerator = args[0].numerator
                self._denominator = args[0].denominator
            elif isinstance(args[0], Unit):
                float_value = ((args[0]._to_base_unit_float()
                                - self._constant_offset)
                               / self._conversion_rate)
                fraction = self._float_to_rounded_fraction_tuple(float_value)
                self._numerator, self._denominator = fraction
            else:
                fraction = self._float_to_rounded_fraction_tuple(args[0])
                self._numerator, self._denominator = fraction
        else:
            raise TypeError('Invalid Beat init signature')

        self._collapsed_fraction = self._as_collapsed_fraction()

        # Calculate base division and dot count
        if isinstance(self.numerator, type(self)):
            self._dot_count = self.numerator.dot_count
            # FIXME: This is wrong !!!
            # Beat(Beat(1, 3), 4) base division should be 8
            # for triplet eighth!
            self._base_division = self.denominator
            self._requires_tie = False
        else:
            dot_count = 0
            partial_numerator = self.collapsed_fraction.numerator
            partial_denominator = self.collapsed_fraction.denominator
            while partial_numerator > 1:
                partial_numerator = (partial_numerator - 1) / 2
                partial_denominator = partial_denominator / 2
                dot_count += 1
            if partial_numerator != 1:
                self._requires_tie = True
            else:
                self._requires_tie = False
            self._base_division = int(partial_denominator)
            self._dot_count = dot_count

    ######## CONSTRUCTORS ########

    @classmethod
    def from_float(cls, value, round_to=None, limit_denominator=1024):
        """Initialize from a float with an optional denominator to round toward.

        Args:
            value (float):
            round_to (int): A denominator to round toward.
            limit_denominator (int): The maximum denominator value.
                If `round_to` is specified, this does nothing.

        Returns: Beat

        Examples:
            >>> Beat.from_float(0.4)
            Beat(2, 5)[Abstract]
            >>> Beat.from_float(0.4, 2)
            Beat(1, 2)[Abstract]
            >>> Beat.from_float(0.4, 4)
            Beat(2, 4)[Abstract]
        """
        fraction_tuple = cls._float_to_rounded_fraction_tuple(
            value,
            round_to,
            limit_denominator)
        return cls(*fraction_tuple)

    @classmethod
    def _from_rhythmic_beat(cls, beat):
        """Initialize a Beat from an existing one taking its fractional value.

        This is distinct from Beat(some_beat) because while the ratio of one
        beat to another in graphical conversion rates may vary, this literally
        copies the fractional value from one beat into a new one
        (whose graphical conversion rate may be different).

        Returns: Beat

        Example:
            >>> LargeSizeBeat = Beat.make_concrete_beat(100)
            >>> SmallSizeBeat = Beat.make_concrete_beat(10)
            >>> large_beat = LargeSizeBeat(1, 4)
            >>> Unit(large_beat)
            Unit(25)
            >>> small_beat = SmallSizeBeat._from_rhythmic_beat(large_beat)
            >>> small_beat.numerator
            1
            >>> small_beat.denominator
            4
            >>> Unit(small_beat)
            Unit(2.5)
        """
        numerator = beat.numerator
        # Recursively convert any nested numerator
        if isinstance(numerator, Beat):
            numerator = cls._from_rhythmic_beat(numerator)
        return cls(numerator, beat.denominator)

    ######## PUBLIC PROPERTIES ########

    @property
    def value(self):
        return float(self.collapsed_fraction)

    @property
    def requires_tie(self):
        """bool: If this Beat requires a tie to be written."""
        return self._requires_tie

    @property
    def numerator(self):
        """int or Beat.

        This property is read-only.
        """
        return self._numerator

    @property
    def denominator(self):
        """int.

        This property is read-only.
        """
        return self._denominator

    @property
    def dot_count(self):
        """int: The number of dots this beat has."""
        return self._dot_count

    @property
    def base_division(self):
        """int: The basic division of the beat."""
        return self._base_division

    @property
    def collapsed_fraction(self):
        """Fraction: The collapsed int / int Fraction of this Beat."""
        return self._collapsed_fraction

    ######## SPECIAL METHODS ########

    def __repr__(self):
        if self._conversion_rate is not None:
            return "{}({}, {})[conversion_rate={}]".format(
                type(self).__name__,
                self.numerator,
                self.denominator,
                self._conversion_rate)
        else:
            return "{}({}, {})[Abstract]".format(
                type(self).__name__,
                self.numerator,
                self.denominator)

    def __hash__(self):
        return hash(self.__repr__())

    def __float__(self):
        """Reduce the fractional representation to a float and return it."""
        return float(self.collapsed_fraction)

    def __eq__(self, other):
        """Two beats are equivalent if their numerators and denominators are."""
        if not isinstance(other, type(self)):
            return super().__eq__(other)
        return (self.numerator == other.numerator and
                self.denominator == other.denominator)

    def __gt__(self, other):
        """Beats are compared by their reduced fraction representations."""
        if not isinstance(other, type(self)):
            return super().__gt__(other)
        return self.collapsed_fraction > other.collapsed_fraction

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            return super().__ge__(other)
        return self > other or self.collapsed_fraction == other.collapsed_fraction

    ######## PRIVATE METHODS ########

    @staticmethod
    def _float_to_rounded_fraction_tuple(value,
                                         round_to=None,
                                         limit_denominator=1024):
        """Make a rounded fraction tuple from a float.

        Args:
            value (float):
            round_to (int): A denominator to round toward.
            limit_denominator (int): The maximum denominator value.
                If `round_to` is specified, this does nothing.

        Returns: tuple(numerator, denominator)

        Examples:
            >>> Beat._float_to_rounded_fraction_tuple(0.4)
            (2, 5)
            >>> Beat._float_to_rounded_fraction_tuple(0.4, 2)
            (1, 2)
            >>> Beat._float_to_rounded_fraction_tuple(0.4, 4)
            (2, 4)
        """
        fraction = Fraction(value).limit_denominator(limit_denominator)
        if round_to is None:
            return (fraction.numerator, fraction.denominator)

        multiplier = round_to / fraction.denominator
        return (
            int(round(multiplier * fraction.numerator)),
            round_to
        )

    def _to_base_unit_float(self):
        """Return this value as a float in base unit values.

        Returns: float
        """
        if self._conversion_rate is None:
            raise AbstractBeatConversionError
        if self._constant_offset:
            return ((self.value * self._conversion_rate)
                    + Unit(self._constant_offset).value)
        else:
            return self.value * self._conversion_rate

    def _as_collapsed_fraction(self):
        """Collapse this Beat into a single Fraction and return it.

        This recursively collapses any nested Beats and simplifies
        the returned Fraction.

        Returns: Fraction
        """
        if isinstance(self.numerator, type(self)):
            return Fraction(self.numerator.collapsed_fraction, self.denominator)
        return Fraction(self.numerator, self.denominator)

    ######## PUBLIC METHODS ########

    @classmethod
    def make_concrete_beat(cls,
                           whole_note_size,
                           constant_offset=None,
                           name=None):
        """Make a concrete Beat class and return it.

        Args:
            whole_note_size (Unit): The length of a Beat(1, 1)
            constant_offset (Unit): A constant offset for all conversions.
            name (str): The name for the concrete Beat class.
                If not specified, 'ConcreteBeat' is used.

        Returns: type
        """
        class FactoryBeat(cls):
            _conversion_rate = Unit(whole_note_size).value
            _constant_offset = (Unit(constant_offset).value if constant_offset
                                else 0)

        FactoryBeat.__name__ = name if name else 'ConcreteBeat'
        return FactoryBeat
