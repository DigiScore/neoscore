import warnings
from typing import Optional, Union, cast

from neoscore.core.mapping import map_between
from neoscore.core.music_text import MusicText
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.western.accidental_type import AccidentalType
from neoscore.western.key_signature_type import KeySignatureType
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject

# TODO LOW this doesn't support natural (cancelling) key signatures


class KeySignature(PositionedObject, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given ``pos_x``,
    and at the beginning of subsequent lines until a new
    ``KeySignature`` is encountered.
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
        PositionedObject.__init__(self, Point(pos_x, ZERO), staff)
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
        """Key signatures extend until another is found in the staff."""
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

    This should only be used by ``KeySignature``.
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

    def render_occurrence(
        self, pos: Point, local_start_x: Optional[Unit], dist_to_line_start: Unit
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
        if dist_to_line_start == ZERO:
            # Note that this doesn't work on the first line if the key sign isn't placed
            # at x=0. We really need proper staff-left-margin handling for this kind of
            # thing.
            visual_pos_x += self._padded_clef_width(clef)
        self.render_slice(Point(visual_pos_x, visual_pos_y))

    def render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        self.render_occurrence(pos, local_start_x, cast(Unit, dist_to_line_start))

    def render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        self.render_occurrence(start, local_start_x, dist_to_line_start)

    def render_after_break(self, local_start_x: Unit, start: Point):
        self.render_occurrence(start, local_start_x, ZERO)

    def render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self.render_occurrence(start, local_start_x, ZERO)
