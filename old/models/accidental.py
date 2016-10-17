class Accidental:
    """
    A simple class containing enumerations relevant to the various accidentals.

    Notes: This is not a StaffObject. For an accidental to be actually drawn, use AccidentalObject.
    """

    # TODO: implement quarter-tone and custom accidentals
    def __init__(self, name):
        """
        Creates the name of the specified type

        Args:
            name (str):
        """
        if not isinstance(name, str):
            raise TypeError('name must be a str')
        # Make sure the name is valid
        name = name.lower()
        if name not in ['double flat', 'flat', 'natural', 'sharp', 'double sharp']:
            raise ValueError('name must be either "double flat", '
                             '"flat", "natural", "sharp", or "double sharp"')

        self.name = name
        if self.name == 'double flat':
            self.pitch_offset = -2
            self.unicode_value = "\uE137"
        elif self.name == 'flat':
            self.pitch_offset = -1
            self.unicode_value = "\uE12E"
        elif self.name == 'natural':
            self.pitch_offset = 0
            self.unicode_value = "\uE14F"
        elif self.name == 'sharp':
            self.pitch_offset = 1
            self.unicode_value = "\uE170"
        elif self.name == 'double sharp':
            self.pitch_offset = 2
            self.unicode_value = "\uE125"

    def __eq__(self, other):
        """
        Test equality between self and another object.

            * if other is an Accidental, compare other.name and self.name
            * if other is a str, compare other to self.name
            * if other is None and self.name == 'natural', return True
            * Otherwise return False

        Args:
            other (Any):

        Returns: bool

        """
        if isinstance(other, Accidental):
            other_name = other.name
        elif isinstance(other, str):
            other_name = other
        elif other is None and self.name == 'natural':
            return True
        else:
            return False
        return other_name == self.name
