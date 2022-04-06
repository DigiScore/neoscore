from __future__ import annotations

from typing import Optional, cast

from neoscore.core.mapping import map_between
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.western import notehead_tables
from neoscore.western.duration import Duration, DurationDef
from neoscore.western.duration_display import DurationDisplay
from neoscore.western.notehead_tables import NoteheadTable
from neoscore.western.pitch import Pitch, PitchDef
from neoscore.western.staff_object import StaffObject


class Notehead(MusicText, StaffObject):

    """A simple notehead automatically selected and vertically positioned."""

    def __init__(
        self,
        pos_x: Unit,
        parent: PositionedObject,
        pitch: PitchDef,
        duration: DurationDef,
        font: Optional[MusicFont] = None,
        notehead_table: NoteheadTable = notehead_tables.STANDARD,
    ):
        """
        Args:
            pos_x: The x-axis position relative to `parent`.
                The y-axis position is calculated automatically based
                on `pitch` and contextual information in `self.staff`.
            parent: Must either be a `Staff` or an object
                with an ancestor `Staff`.
            pitch: May be a `str` pitch representation.
                See `Pitch` for valid signatures.
            duration: The logical duration of
                the notehead. This is used to determine the glyph style.
            font: If provided, this overrides any font found in the ancestor chain.
            notehead_table: The set of noteheads to use according to `duration`.
        """
        self._pitch = Pitch.from_def(pitch)
        self.duration = Duration.from_def(duration)
        self._notehead_table = notehead_table
        duration_display = cast(DurationDisplay, self.duration.display)
        # Use a temporary y-axis position before calculating it for real
        MusicText.__init__(
            self,
            (pos_x, ZERO),
            parent,
            self._notehead_table.lookup_duration(duration_display.base_duration),
            font,
        )
        StaffObject.__init__(self, parent)
        self.y = self.staff.unit(
            self.staff_pos - map_between(self.staff, self.parent).y
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def visual_width(self) -> Unit:
        """The visual width of the Notehead"""
        return self.bounding_rect.width

    # TODO MEDIUM make these setter update glyph / pos

    @property
    def pitch(self) -> Pitch:
        """The logical pitch."""
        return self._pitch

    @pitch.setter
    def pitch(self, value: PitchDef):
        self._pitch = Pitch.from_def(value)

    @property
    def duration(self) -> Duration:
        """The time duration of this Notehead"""
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value

    @property
    def staff_pos(self) -> Unit:
        """The y-axis position in the staff.

        0 means the top staff line, higher values mean lower pitches,
        and vice versa.
        """
        return self.staff.middle_c_at(self.pos_x_in_staff) + self.staff.unit(
            self.pitch.staff_pos_from_middle_c
        )
