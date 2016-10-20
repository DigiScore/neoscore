class InvalidAccidentalError(Exception):
    """Exception thrown when an invalid accidental descriptor is requested."""
    pass


class Accidental:

    def __init__(self, value):
        """
        Args:
            value (str or int or None): A description of the accidental.
                'f' or -1: Flat
                'n' or  0: Natural (Explicit)
                's' or  1: Sharp
                None     : No accidental, value depends on context.
        """
        self.value = value

    ######## PUBLIC PROPERTIES ########

    @property
    def value(self):
        """int or None: The value of the accidental.

        String values passed to this will be automatically converted
        to their integer representations. None values will remain None.

        'f' or -1: Flat
        'n' or  0: Natural (Explicit)
        's' or  1: Sharp
        None     : No accidental, value depends on context.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, str):
            if new_value == 'f':
                self._value = -1
            elif new_value == 'n':
                self._value = 0
            elif new_value == 's':
                self._value = 1
            else:
                raise InvalidAccidentalError
        elif isinstance(new_value, (int, float)):
            if -1 <= new_value <= 1:
                self._value = int(new_value)
            else:
                raise InvalidAccidentalError
        elif new_value is None:
            self._value = None
        else:
            raise InvalidAccidentalError
