from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.models.accidental_type import AccidentalType
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Accidental(MusicText):

    """A visual accidental."""

    _canonical_names = {
        AccidentalType.FLAT: "accidentalFlat",
        AccidentalType.NATURAL: "accidentalNatural",
        AccidentalType.SHARP: "accidentalSharp",
    }

    def __init__(
        self,
        pos: PointDef,
        parent: Parent,
        accidental_type: AccidentalType,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: Position relative to `parent`
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            accidental_type: the accidental to draw
            font: If provided, this overrides any font found in the ancestor chain.
        """
        self._accidental_type = accidental_type
        canonical_name = self._canonical_names[self.accidental_type]
        MusicText.__init__(self, pos, parent, [canonical_name], font)

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
        # ((later update - i think this is unblocked now))
        self._accidental_type = value
