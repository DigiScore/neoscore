from brown.core.music_text import MusicText
from brown.models.virtual_accidental import VirtualAccidental
from brown.utils.exceptions import InvalidVirtualAccidentalError


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
            kind (VirtualAccidental or str): The type of accidental.
                For convenience, any `str` of a `VirtualAccidental`
                enum name may be passed.
            parent (StaffObject or Staff):
        """
        if isinstance(kind, VirtualAccidental):
            self.virtual_accidental = kind
        else:
            try:
                self.virtual_accidental = VirtualAccidental[kind]
            except KeyError:
                raise InvalidVirtualAccidentalError
        canonical_name = self._canonical_names[self.virtual_accidental.name]
        super().__init__(pos, [canonical_name], parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def virtual_accidental(self):
        """VirtualAccidental: What type of accidental this is."""
        return self._virtual_accidental

    @virtual_accidental.setter
    def virtual_accidental(self, value):
        self._virtual_accidental = value
