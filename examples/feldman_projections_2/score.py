from typing import Union

from brown import constants
from brown.core import brown
from brown.core.font import Font
from brown.core.music_font import MusicFont
from brown.core.object_group import ObjectGroup
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.pen_pattern import PenPattern
from brown.core.staff import Staff
from brown.utils.units import GraphicUnit
from examples.feldman_projections_2.glyph_name import GlyphName
from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.instrument_data import InstrumentData
from examples.feldman_projections_2.measure import Measure
from examples.feldman_projections_2.music_text_event import MusicTextEvent
from examples.feldman_projections_2.text_event import TextEvent


class Score(ObjectGroup):

    _TEXT_FONT_SIZE = GridUnit(0.6).base_value
    _MUSIC_FONT_SIZE = Staff._make_unit_class(GridUnit(0.5))

    _bar_line_pen = Pen(thickness=GridUnit(0.05), pattern=PenPattern.DOT)
    _instrument_divider_pen = Pen(thickness=GridUnit(0.05))

    def __init__(self, pos, instruments, parent):
        super().__init__(pos, parent)
        self.events = []
        self.text_font = Font.deriving(
            brown.default_font, size=Score._TEXT_FONT_SIZE, weight=60
        )
        self.music_font = MusicFont(
            constants.DEFAULT_MUSIC_FONT_NAME, Score._MUSIC_FONT_SIZE
        )

        self.instruments = instruments

        for i, instrument in enumerate(instruments):
            for event_data in instrument.event_data:
                self.events.append(self._create_event(i, event_data))

        self.draw_instrument_dividers()
        self.draw_bar_lines()

    def _create_event(self, instrument_index, event_data):
        if isinstance(event_data.text, GlyphName):
            return self._create_music_text_event(instrument_index, event_data)
        return self._create_text_event(instrument_index, event_data)

    def _create_text_event(self, instrument_index, event_data):
        return TextEvent(
            (
                event_data.pos_x,
                (Score._instrument_pos_y(instrument_index) + event_data.register.value),
            ),
            self,
            event_data.length,
            event_data.text,
            self.text_font,
        )

    def _create_music_text_event(self, instrument_index, event_data):
        return MusicTextEvent(
            (
                event_data.pos_x,
                (Score._instrument_pos_y(instrument_index) + event_data.register.value),
            ),
            self,
            event_data.length,
            event_data.text,
            self.music_font,
        )

    @property
    def measure_count(self):
        return (
            max(
                max(int(Measure(e.pos_x).display_value) for e in i.event_data)
                for i in self.instruments
            )
            + 1
        )

    @staticmethod
    def _instrument_pos_y(instrument_index):
        return GridUnit(3 * instrument_index)

    @staticmethod
    def _divider_pos_y(divider_index):
        return GridUnit(3 * divider_index)

    @staticmethod
    def _divider_visible(
        instrument_above: Union[InstrumentData, None],
        instrument_below: Union[InstrumentData, None],
        measure_num: int,
    ) -> bool:
        return (
            instrument_above is not None
            and instrument_above.measure_has_events(measure_num)
        ) or (
            instrument_below is not None
            and instrument_below.measure_has_events(measure_num)
        )

    def _bar_line_extends_below(self, measure_num: int, divider_num: int) -> bool:
        if divider_num >= len(self.instruments):
            return False
        instrument = self.instruments[divider_num]
        return instrument.measure_has_events(
            measure_num - 1
        ) or instrument.measure_has_events(measure_num)

    def draw_instrument_dividers(self):
        for divider in range(len(self.instruments) + 1):
            current_path = Path(
                (Measure(0), Score._divider_pos_y(divider)),
                pen=Score._instrument_divider_pen,
                parent=self,
            )
            instrument_above = self.instruments[divider - 1] if divider > 0 else None
            instrument_below = (
                self.instruments[divider] if divider < len(self.instruments) else None
            )
            drawing = False
            for measure_num in range(self.measure_count + 1):
                if Score._divider_visible(
                    instrument_above, instrument_below, measure_num
                ):
                    if not drawing:
                        current_path.move_to(Measure(measure_num), GridUnit(0))
                        drawing = True
                else:
                    if drawing:
                        current_path.line_to(Measure(measure_num), GridUnit(0))
                        drawing = False

    def draw_bar_lines(self):
        for measure_num in range(self.measure_count + 1):
            current_path = Path(
                (Measure(measure_num), GridUnit(0)),
                pen=Score._bar_line_pen,
                parent=self,
            )
            drawing = False
            for divider_num in range(len(self.instruments) + 1):
                if self._bar_line_extends_below(measure_num, divider_num):
                    if not drawing:
                        current_path.move_to(
                            GridUnit(0), Score._instrument_pos_y(divider_num)
                        )
                        drawing = True
                else:
                    if drawing:
                        current_path.line_to(
                            GridUnit(0), Score._instrument_pos_y(divider_num)
                        )
                        drawing = False
