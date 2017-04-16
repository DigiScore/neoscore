from brown.core.music_text import MusicText
from brown.models.accidental_type import AccidentalType
from brown.utils.exceptions import InvalidAccidentalTypeError


class Accidental(MusicText):

    """A visible accidental."""

    _canonical_names = {
        'flat': 'accidentalFlat',
        'natural':  'accidentalNatural',
        'sharp':  'accidentalSharp',
    }

    def __init__(self, pos, kind, parent):
        """
        Args:
            pos (Point): The position of the accidental
            kind (AccidentalType or str): The type of accidental.
                For convenience, any `str` of a `AccidentalType`
                enum name may be passed.
            parent (StaffObject or Staff):
        """
        if isinstance(kind, AccidentalType):
            self.accidental_type = kind
        else:
            try:
                self.accidental_type = AccidentalType[kind]
            except KeyError:
                raise InvalidAccidentalTypeError
        canonical_name = self._canonical_names[self.accidental_type.name]
        super().__init__(pos, [canonical_name], parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def accidental_type(self):
        """AccidentalType: What type of accidental this is."""
        return self._accidental_type

    @accidental_type.setter
    def accidental_type(self, value):
        self._accidental_type = value
