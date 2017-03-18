from brown.core.music_text import MusicText
from brown.models.virtual_accidental import (VirtualAccidental,
                                             InvalidAccidentalError)
from brown.utils.exceptions import NoneVirtualAccidentalInRealAccidentalError


class Accidental(MusicText):

    _canonical_names = {
        -1: 'accidentalFlat',
        0:  'accidentalNatural',
        1:  'accidentalSharp',
    }

    def __init__(self, pos, kind, parent):
        """
        Args:
            pos (Point): The position of the accidental
            kind (VirtualAccidental, str, int, or None):
                The type of accidental. For convenience, any valid constructor
                argument to VirtualAccidental (except None) may be passed.
                `None` VirtualAccidentals are not accepted.
            parent (StaffObject or Staff):
        """
        try:
            self.virtual_accidental = VirtualAccidental(kind)
            if self.virtual_accidental.value is None:
                raise NoneVirtualAccidentalInRealAccidentalError(
                    "cannot create real Accidental object "
                    "with VirtualAccidental('None')")
        except InvalidAccidentalError as error:
            raise error
        canonical_name = self._canonical_names[self.virtual_accidental.value]
        super().__init__(pos, [canonical_name], parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def virtual_accidental(self):
        """VirtualAccidental: What type of accidental this is."""
        return self._virtual_accidental

    @virtual_accidental.setter
    def virtual_accidental(self, value):
        self._virtual_accidental = value
