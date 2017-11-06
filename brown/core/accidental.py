from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.models.accidental_type import AccidentalType
from brown.utils.exceptions import InvalidAccidentalTypeError


class Accidental(MusicText, StaffObject):

    """A visible accidental."""

    _canonical_names = {
        AccidentalType.flat: 'accidentalFlat',
        AccidentalType.natural:  'accidentalNatural',
        AccidentalType.sharp:  'accidentalSharp',
    }

    def __init__(self, pos, accidental_type, parent):
        """
        Args:
            pos (Point): The position of the accidental
            accidental_type (AccidentalType or str): The type of accidental.
                For convenience, any `str` of a `AccidentalType`
                enum name may be passed.
            parent (StaffObject or Staff):
        """
        if isinstance(accidental_type, AccidentalType):
            self._accidental_type = accidental_type
        else:
            try:
                self._accidental_type = AccidentalType[accidental_type]
            except KeyError:
                raise InvalidAccidentalTypeError
        canonical_name = self._canonical_names[self.accidental_type]
        MusicText.__init__(self, pos, [canonical_name], parent)
        StaffObject.__init__(self, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def accidental_type(self):
        """AccidentalType: What type of accidental this is."""
        return self._accidental_type

    @accidental_type.setter
    def accidental_type(self, value):
        self._accidental_type = value
