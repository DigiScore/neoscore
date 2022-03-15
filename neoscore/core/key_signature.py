from typing import Union

from neoscore.core.accidental import Accidental
from neoscore.core.mapping import map_between
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.core.staff import Staff
from neoscore.core.staff_object import StaffObject
from neoscore.models.accidental_type import AccidentalType
from neoscore.models.clef_type import ClefType
from neoscore.models.key_signature_type import KeySignatureType
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import Unit


class KeySignature(ObjectGroup, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given `pos_x`,
    and at the beginning of subsequent lines until a new
    `KeySignature` is encountered.

    All traditional key signatures (those included in `KeySignatureTypes`)
    are supported by this class. Nontraditional key signatures could
    be implemented in a fairly straightforward way in a subclass of this.
    """

    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        key_signature_type: Union[KeySignatureType, str],
    ):
        """
        Args:
            pos_x (Unit): The x position relative to the parent staff.
            staff (Staff): The parent staff
            key_signature_type (KeySignatureType or str): A description of the
                key signature. Any KeySignatureType may be used, or a str
                of one's name.
        """
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)), staff)
        StaffObject.__init__(self, staff)
        self._key_signature_type = (
            key_signature_type
            if isinstance(key_signature_type, KeySignatureType)
            else KeySignatureType[key_signature_type.upper()]
        )
        self._create_pseudo_accidentals()

    ######## PUBLIC PROPERTIES ########

    @property
    def key_signature_type(self) -> KeySignatureType:
        """KeySignatureType: A logical description of the key signature."""
        return self._key_signature_type

    @property
    def length(self) -> Unit:
        """`KeySignature`s extend until another is found in the staff."""
        return self.staff.distance_to_next_of_type(self)

    ######## PRIVATE METHODS ########

    def _create_pseudo_accidentals(self):
        length = self.length
        for key, value in self.key_signature_type.value.items():
            if value is not None:
                _KeySignatureAccidental(ORIGIN, self, key, value, self.staff.music_font, 1, length)


class _KeySignatureAccidental(MusicText, StaffObject):
    """A visual accidental.

    This should only be used within `KeySignature`s.
    """

    __sharp_positions = {
        "f": (0, 0),
        "c": (1, 1.5),
        "g": (2, -0.5),
        "d": (3, 1),
        "a": (4, 2.5),
        "e": (5, 0.5),
        "b": (6, 2),
    }
    __flat_positions = {
        "b": (0, 2),
        "e": (1, 0.5),
        "a": (2, 2.5),
        "d": (3, 1),
        "g": (4, 3),
        "c": (5, 1.5),
        "f": (6, 3.5),
    }
    positions = {
        AccidentalType.FLAT: {
            ClefType.TREBLE: __flat_positions,
            ClefType.BASS: {
                key: (value[0], value[1] + 1) for key, value in __flat_positions.items()
            },
            ClefType.ALTO: {
                key: (value[0], value[1] + 0.5)
                for key, value in __flat_positions.items()
            },
            ClefType.TENOR: {
                key: (value[0], value[1] - 0.5)
                for key, value in __flat_positions.items()
            },
        },
        AccidentalType.SHARP: {
            ClefType.TREBLE: __sharp_positions,
            ClefType.BASS: {
                key: (value[0], value[1] + 1)
                for key, value in __sharp_positions.items()
            },
            ClefType.ALTO: {
                key: (value[0], value[1] + 0.5)
                for key, value in __sharp_positions.items()
            },
            ClefType.TENOR: {
                key: (value[0], value[1] - 0.5)
                for key, value in __sharp_positions.items()
            },
        },
    }

    def __init__(self, pos, key_signature, pitch_letter, accidental_type, music_font, scale, length):
        MusicText.__init__(self, pos, key_signature, Accidental._canonical_names[accidental_type], music_font, scale)
        StaffObject.__init__(self, key_signature)
        self._length = length
        self.pitch_letter = pitch_letter
        self.accidental_type = accidental_type

    @property
    def length(self):
        return self._length

    def _padded_clef_width(self, clef):
        return clef.bounding_rect.width + self.staff.unit(0.5)

    def _render_occurrence(self, pos: Point, local_start_x: Unit, shift_for_clef: bool):
        """Render one appearance of one key signature accidental.

        Much of the positioning code needs to be performed
        per-occurrence because key signatures can have different
        appearances when clefs change.

        Ideally there should be a way to cache/centralize much of this
        work.

        """
        staff_pos_in_flowable = map_between(self.flowable, self.staff)
        pos_x_in_staff = local_start_x - staff_pos_in_flowable.x
        clef = self.staff.active_clef_at(pos_x_in_staff)
        if clef is None:
            return
        clef_type = clef.clef_type
        pos_tuple = _KeySignatureAccidental.positions[self.accidental_type][clef_type][
            self.pitch_letter
        ]
        visual_pos_x = self.staff.unit(pos_tuple[0]) + pos.x
        visual_pos_y = self.staff.unit(pos_tuple[1]) + pos.y
        if shift_for_clef:
            visual_pos_x += self._padded_clef_width(clef)
        self._render_slice(Point(visual_pos_x, visual_pos_y))

    def _render_complete(self, pos, dist_to_line_start=None, local_start_x=None):
        self._render_occurrence(pos, local_start_x, False)

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self._render_occurrence(start, local_start_x, False)

    def _render_after_break(self, local_start_x, start):
        self._render_occurrence(start, local_start_x, True)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_occurrence(start, local_start_x, True)
