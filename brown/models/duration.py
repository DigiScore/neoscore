from fractions import Fraction


class Duration:
    """A duration in a meter whose value is measured in rational numbers.

    The duration fraction indicates duration as a fraction of a whole note.
    The actual written denomination of duration is deduced
    from the reduced fraction. For instance:

    * `Duration(1, 4)` indicates a quarter note value
    * `Duration(1, 1)` indicates a whole note value
    * `Duration(3, 8)` indicates a dotted quarter note value

    Arbitrarily nested tuplets can be created by nesting Durations
    in each other. To do this, let the numerator of a Duration
    be a Duration where the denominator indicates the division
    within the outer Duration. The actual written denomination
    of the durataion is inferred.

    * `Duration(Duration(1, 3), 4)` indicates an eighth in a triplet
      spanning a quarter
    * `Duration(Duration(1, 5), 8)` indicates a 32nd in a quintuplet
      spanning an eighth
    * `Duration(Duration(2, 10), 8)` is equivalent to
      `Duration(Duration(1, 5), 8)` seen above, for the same reason
      that `Duration(2, 8)` is equivalent to `Duration(1, 4)`
    * `Duration(Duration(3, 10), 8)` indicates a dotted 32nd in a quintuplet
      spanning an eighth.

    Nested Durations are not reduced into each other:
    * `Duration(Duration(1, 2), 4)` is *not* equivalent to `Duration(1, 8)`

    Durations should be treated as immutable, and will not work correctly
    if their properties are changed after initialization.

    # TODO: How to handle things like duplet over dotted quarter?
    """

    def __init__(self, numerator, denominator):
        """
        Args:
            numerator (int or Duration):
            denominator (int):
        """
        self._numerator = numerator
        self._denominator = denominator
        self._simplify()
        self._collapsed_fraction = self._as_collapsed_fraction()

        # Calculate base division and dot count
        if isinstance(self.numerator, type(self)):
            self._dot_count = self.numerator.dot_count
            # FIXME: This is wrong !!!
            # Duration(Duration(1, 3), 4) base division should be 8
            # for triplet eighth!
            self._base_division = self.denominator
            self._requires_tie = False
        else:
            dot_count = 0
            partial_numerator = self.numerator
            partial_denominator = self.denominator
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

    ######## PUBLIC PROPERTIES ########

    @property
    def requires_tie(self):
        """bool: If this Duration requires a tie to be written."""
        return self._requires_tie

    @property
    def numerator(self):
        """int or Duration.

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
        """int: The number of dots this duration has."""
        return self._dot_count

    @property
    def base_division(self):
        """int: The basic division of the duration."""
        return self._base_division

    @property
    def collapsed_fraction(self):
        """Fraction: The collapsed int / int Fraction of this Duration."""
        return self._collapsed_fraction

    ######## SPECIAL METHODS ########

    def __repr__(self):
        """Represent the Duration as its init signature"""
        return "{}({}, {})".format(type(self).__name__,
                                   self.numerator,
                                   self.denominator)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        """Two durations are equivalent if their numerators and denominators are."""
        if not isinstance(other, type(self)):
            return False
        return (self.numerator == other.numerator and
                self.denominator == other.denominator)

    def __gt__(self, other):
        """Durations are compared by their reduced fraction representations."""
        return self.collapsed_fraction > other.collapsed_fraction

    def __ge__(self, other):
        return self > other or self.collapsed_fraction == other.collapsed_fraction

    ######## PRIVATE METHODS ########

    def _simplify(self):
        """Simplify this Duration if it is non-nested

        Returns: None
        """
        if isinstance(self.numerator, type(self)):
            return
        else:
            reduced = Fraction(self.numerator, self.denominator)
            self._numerator = reduced.numerator
            self._denominator = reduced.denominator

    def _as_collapsed_fraction(self):
        """Collapse this Duration into a single Fraction and return it.

        This recursively collapses any nested Durations and simplifies
        the returned Fraction.

        Returns: Fraction
        """
        if isinstance(self.numerator, type(self)):
            return Fraction(self.numerator.collapsed_fraction, self.denominator)
        return Fraction(self.numerator, self.denominator)
