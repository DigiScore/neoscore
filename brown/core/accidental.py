from brown.core.graphic_object import GraphicObject
from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.models.accidental_type import AccidentalType
from brown.utils.point import PointDef


class Accidental(MusicText, StaffObject):

    """A visual accidental."""

    _canonical_names = {
        AccidentalType.FLAT: "accidentalFlat",
        AccidentalType.NATURAL: "accidentalNatural",
        AccidentalType.SHARP: "accidentalSharp",
    }

    def __init__(
        self, pos: PointDef, accidental_type: AccidentalType, parent: GraphicObject
    ):
        self._accidental_type = accidental_type
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
        # TODO MEDIUM this needs to update the underlying text. This
        # can't currently be done because MusicText doesn't support
        # changing the text.
        self._accidental_type = value
