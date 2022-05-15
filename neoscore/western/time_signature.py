from __future__ import annotations

from typing import Optional

from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.text_alignment import AlignmentX
from neoscore.core.units import ZERO, Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.meter import Meter, MeterDef
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class TimeSignature(PositionedObject, StaffObject):

    """A graphical time signature.

    Note that these time signatures are purely cosmetic; they have no effect on
    automatic engraving since this module has no internal concept of measures.
    """

    # Type sentinel used to hackily check type
    # without importing the type, risking cyclic imports.
    _neoscore_time_signature_type_marker = True

    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        meter: MeterDef,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos_x: The x position relative to the parent staff
            staff: The parent staff
            meter: The meter represented.
            font: The font used. Defaults to the staff's font.
        """
        StaffObject.__init__(self, staff)
        PositionedObject.__init__(self, Point(pos_x, ZERO), staff)
        font = font or staff.music_font
        self._meter = Meter.from_def(meter)
        # Add one glyph for each digit
        self._upper_text = _TimeSignatureText(
            self.staff,
            self.x,
            ORIGIN,
            self,
            self.meter.upper_text_glyph_names,
            font=font,
            breakable=False,
        )
        self._lower_text = _TimeSignatureText(
            self.staff,
            self.x,
            ORIGIN,
            self,
            self.meter.lower_text_glyph_names,
            font=font,
            breakable=False,
        )
        self._position_glyphs()

    @property
    def upper_text(self) -> MusicText:
        """The upper glyph for the time signature"""
        return self._upper_text

    @property
    def lower_text(self) -> MusicText:
        """The lower glyph for the time signature"""
        return self._lower_text

    @property
    def visual_width(self) -> Unit:
        """The visual width of the time signature.

        This is useful for laying out staff objects near time signatures.
        """
        return self._visual_width

    @property
    def meter(self) -> Meter:
        """The meter represented.

        Setting this will automatically update the time signature's glyphs.
        """
        return self._meter

    @meter.setter
    def meter(self, value: MeterDef):
        self._meter = Meter.from_def(value)
        self.upper_text.text = self._meter.upper_text_glyph_names
        self.lower_text.text = self._meter.lower_text_glyph_names
        self._position_glyphs()

    def _position_glyphs(self):
        """This must be called after any modification to the glyph text"""
        # Vertically position, assuming time sig glyphs are 2 units tall and centered
        staff_center_y = self.staff.center_y
        if not self.meter.lower_text_glyph_names:
            self.upper_text.y = staff_center_y
        else:
            self.upper_text.y = staff_center_y - self.staff.unit(1)
            self.lower_text.y = staff_center_y + self.staff.unit(1)
        # Horizontally position
        upper_width = self.upper_text.bounding_rect.width
        lower_width = self.lower_text.bounding_rect.width
        if upper_width > lower_width:
            self._visual_width = upper_width
            self.lower_text.x += upper_width / 2
            self.lower_text.alignment_x = AlignmentX.CENTER
        elif lower_width > upper_width:
            self._visual_width = lower_width
            self.upper_text.x += lower_width / 2
            self.upper_text.alignment_x = AlignmentX.CENTER
        else:
            # Widths are equal. No adjustment needed.
            self._visual_width = upper_width


class _TimeSignatureText(MusicText):

    """A regular MusicText with special rendering behavior in staff fringes.

    If this text is rendered at the very beginning of a staff, it will shift according
    to the staff's fringe layout.
    """

    def __init__(
        self,
        staff: Optional[AbstractStaff],
        staff_pos_x: Optional[Unit],
        *args,
        **kwargs,
    ):
        self.staff = staff
        self.staff_pos_x = staff_pos_x
        super().__init__(*args, **kwargs)

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        if self.staff_pos_x == ZERO:
            fringe_layout = self.staff.fringe_layout_at(None)
            pos = Point(pos.x + fringe_layout.time_signature, pos.y)
        super().render_complete(pos, flowable_line, flowable_x)
