from __future__ import annotations

from typing import Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject, render_cached_property
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
        table: NoteheadTable = notehead_tables.STANDARD,
        glyph_override: Optional[str] = None,
    ):
        """
        Args:
            pos_x: The x-axis position relative to ``parent``.
                The y-axis position is calculated automatically based
                on ``pitch`` and contextual information in ``self.staff``.
            parent: Must be a :obj:`.Staff` or a descendant of one.
            pitch: The pitch used to vertically place the notehead.
                See :obj:`.Pitch` and :obj:`.PitchDef`
            duration: The logical duration of the notehead. This is used to determine
                the glyph style.
            font: If provided, this overrides any font found in the ancestor chain.
            table: The set of noteheads to use according to ``duration``.
                See :obj:`.notehead_tables`.
            glyph_override: A SMuFL glyph name. If given, this overrides
                the glyph normally looked up with ``duration`` from ``table``.
        """
        self.pitch = pitch
        self.duration = duration
        self._table = table
        self._glyph_override = glyph_override
        MusicText.__init__(
            self,
            (pos_x, ZERO),
            parent,
            "",
            font,
        )
        StaffObject.__init__(self, parent)
        self._update_music_text()

    @property
    def visual_width(self) -> Unit:
        return self.bounding_rect.width

    @property
    def pitch(self) -> Pitch:
        return self._pitch

    @pitch.setter
    def pitch(self, value: PitchDef):
        rebuild_needed = hasattr(self, "_pitch")
        self._pitch = Pitch.from_def(value)
        if rebuild_needed:
            self._update_music_text()

    @property
    def duration(self) -> Duration:
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        rebuild_needed = hasattr(self, "_duration")
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value
        if rebuild_needed:
            self._update_music_text()

    @property
    def table(self) -> NoteheadTable:
        return self._table

    @table.setter
    def table(self, value: NoteheadTable):
        self._table = value
        self._update_music_text()

    @property
    def glyph_override(self) -> Optional[str]:
        return self._glyph_override

    @glyph_override.setter
    def glyph_override(self, value: Optional[str]):
        self._glyph_override = value
        self._update_music_text()

    @render_cached_property
    def staff_pos(self) -> Unit:
        """The y-axis position in the staff.

        This is derived from the ``pitch`` and the staff's active clef at this object's
        position.
        """
        return self.staff.middle_c_at(self.pos_x_in_staff) + self.staff.unit(
            self.pitch.staff_pos_from_middle_c
        )

    def _update_music_text(self):
        duration_display = cast(DurationDisplay, self.duration.display)
        if self._glyph_override:
            glyph = self._glyph_override
        else:
            glyph = self._table.lookup_duration(duration_display.base_duration)
        self.text = glyph
        self.y = self.staff_pos - self.staff.map_to(self.parent).y
