from typing import Optional, Union

from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_text import MusicText
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.units import ZERO, Unit
from neoscore.western import clef_type
from neoscore.western.accidental_type import AccidentalType
from neoscore.western.key_signature_type import KeySignatureType
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class KeySignature(PositionedObject, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given ``pos_x``,
    and at the beginning of subsequent lines until a new
    ``KeySignature`` is encountered.

    This does not currently support natural (cancelling key signatures).
    """

    # Type sentinel used to hackily check type
    # without importing the type, risking cyclic imports.
    _neoscore_key_signature_type_marker = True

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

    @property
    def key_signature_type(self) -> KeySignatureType:
        """KeySignatureType: A logical description of the key signature."""
        return self._key_signature_type

    @property
    def breakable_length(self) -> Unit:
        """Key signatures extend until another is found in the staff."""
        return self.staff.distance_to_next_of_type(self)

    @render_cached_property
    def visual_width(self) -> Unit:
        """The visual width of this key signature

        This assumes that key signatures have the same width in any clef, and that the
        accidentals used in key signatures are 1 staff unit wide.
        """
        max_x = 0
        for letter, accidental_type in self.key_signature_type.value.items():
            if accidental_type is None:
                continue
            if accidental_type == AccidentalType.SHARP:
                pos_tuple = clef_type.TREBLE.key_signature_sharp_layout[letter]
            else:
                pos_tuple = clef_type.TREBLE.key_signature_flat_layout[letter]
            max_x = max(max_x, pos_tuple[0])
        # Add max position + 1 for accidental width
        return self.staff.unit(max_x + 1)

    def _render_occurrence(
        self, pos: Point, flowable_line: Optional[NewLine], for_line_start: bool
    ):
        inside_flowable = bool(flowable_line)
        # when inside flowable this pos is absolute, otherwise relative
        base_x = pos.x
        base_y = pos.y
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        if for_line_start:
            base_x += fringe_layout.key_signature
        clef = self.staff.active_clef_at(fringe_layout.pos_x_in_staff)
        for letter, accidental_type in self.key_signature_type.value.items():
            if accidental_type is None:
                continue
            if accidental_type == AccidentalType.SHARP:
                pos_tuple = clef.clef_type.key_signature_sharp_layout[letter]
            else:
                pos_tuple = clef.clef_type.key_signature_flat_layout[letter]
            acc_pos = Point(
                base_x + self.staff.unit(pos_tuple[0]),
                base_y + self.staff.unit(pos_tuple[1]),
            )
            parent = None if inside_flowable else self
            accidental = MusicText(
                acc_pos, parent, accidental_type.value, self.staff.music_font
            )
            accidental.render()
            accidental.remove()

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        for_line_start = False
        if flowable_line:
            if flowable_line.flowable_x == flowable_x:
                for_line_start = True
        elif self.x == ZERO:
            for_line_start = True
        self._render_occurrence(pos, flowable_line, for_line_start)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        for_line_start = fringe_layout.pos_x_in_staff == self.pos_x_in_staff
        self._render_occurrence(pos, flowable_line, for_line_start)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_occurrence(pos, flowable_line, True)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_occurrence(pos, flowable_line, True)
