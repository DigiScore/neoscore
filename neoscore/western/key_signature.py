import warnings
from typing import Optional, Union

from neoscore.core.mapping import map_between
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.models.accidental_type import AccidentalType
from neoscore.models.key_signature_type import KeySignatureType
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import Unit
from neoscore.western import clef_type
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject

# TODO LOW this doesn't support natural (cancelling) key signatures


class KeySignature(ObjectGroup, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given `pos_x`,
    and at the beginning of subsequent lines until a new
    `KeySignature` is encountered.
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
    def breakable_length(self) -> Unit:
        """`KeySignature`s extend until another is found in the staff."""
        return self.staff.distance_to_next_of_type(self)

    ######## PRIVATE METHODS ########

    def _create_pseudo_accidentals(self):
        length = self.breakable_length
        for key, value in self.key_signature_type.value.items():
            if value is not None:
                _KeySignatureAccidental(
                    ORIGIN, self, key, value, self.staff.music_font, 1, length
                )


class _KeySignatureAccidental(MusicText, StaffObject):
    """A visual accidental.

    This should only be used within `KeySignature`s.
    """

    def __init__(
        self,
        pos,
        key_signature,
        pitch_letter,
        accidental_type,
        music_font,
        scale,
        length,
    ):
        MusicText.__init__(
            self,
            pos,
            key_signature,
            accidental_type.value,
            music_font,
            scale=scale,
        )
        StaffObject.__init__(self, key_signature)
        self._length = length
        self.pitch_letter = pitch_letter
        self.accidental_type = accidental_type

    @property
    def breakable_length(self):
        return self._length

    def _padded_clef_width(self, clef):
        return clef.bounding_rect.width + self.staff.unit(0.5)

    def _render_occurrence(
        self, pos: Point, local_start_x: Optional[Unit], shift_for_clef: bool
    ):
        """Render one appearance of one key signature accidental.

        Much of the positioning code needs to be performed
        per-occurrence because key signatures can have different
        appearances when clefs change.

        Ideally there should be a way to cache/centralize much of this
        work.

        """
        if local_start_x is not None:
            staff_pos_in_flowable = map_between(self.flowable, self.staff)
            pos_x_in_staff = local_start_x - staff_pos_in_flowable.x
        else:
            pos_x_in_staff = map_between(self.staff, self).x
        clef = self.staff.active_clef_at(pos_x_in_staff)
        if clef is None:
            return
        clef_type = clef.clef_type
        try:
            if self.accidental_type == AccidentalType.SHARP:
                pos_tuple = clef_type.key_signature_sharp_layout[self.pitch_letter]
            else:
                pos_tuple = clef_type.key_signature_flat_layout[self.pitch_letter]
        except TypeError:
            warnings.warn(
                f"Clef {clef_type} does not support key signatures; skipping this occurrence."
            )
            return
        visual_pos_x = self.staff.unit(pos_tuple[0]) + pos.x
        visual_pos_y = self.staff.unit(pos_tuple[1]) + pos.y
        if shift_for_clef:
            visual_pos_x += self._padded_clef_width(clef)
        self._render_slice(Point(visual_pos_x, visual_pos_y))

    def _render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        self._render_occurrence(pos, local_start_x, False)

    def _render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        self._render_occurrence(start, local_start_x, False)

    def _render_after_break(self, local_start_x: Unit, start: Point):
        self._render_occurrence(start, local_start_x, True)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_occurrence(start, local_start_x, True)
