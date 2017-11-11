from brown import config
from brown.core import brown
from brown.core.music_font import MusicFont
from brown.core.object_group import ObjectGroup
from brown.core.font import Font
from brown.core.staff import Staff
from brown.utils.units import GraphicUnit
from examples.feldman_projections_2.glyph_name import GlyphName
from examples.feldman_projections_2.text_event import TextEvent
from examples.feldman_projections_2.music_text_event import MusicTextEvent
from examples.feldman_projections_2.grid_unit import GridUnit


class Score(ObjectGroup):

    _TEXT_FONT_SIZE = GraphicUnit(GridUnit(0.5)).value
    _MUSIC_FONT_SIZE = Staff._make_unit_class(GridUnit(0.5))

    def __init__(self, pos, instruments):
        super().__init__(pos)
        self.events = []
        self.text_font = Font.deriving(
            brown.default_font,
            size=Score._TEXT_FONT_SIZE)
        self.music_font = MusicFont(
            config.DEFAULT_MUSIC_FONT_NAME,
            Score._MUSIC_FONT_SIZE)

        for i, instrument in enumerate(instruments):
            for event_data in instrument.event_data:
                self.events.append(self._create_event(i, event_data))

    def _create_event(self, instrument_index, event_data):
        if isinstance(event_data.text, GlyphName):
            return self._create_music_text_event(instrument_index, event_data)
        return self._create_text_event(instrument_index, event_data)

    def _create_text_event(self, instrument_index, event_data):
        return TextEvent(
            (event_data.pos_x, (Score._instrument_pos_y(instrument_index)
                                + event_data.register.value)),
            self,
            event_data.length,
            event_data.text,
            self.text_font)

    def _create_music_text_event(self, instrument_index, event_data):
        return MusicTextEvent(
            (event_data.pos_x, (Score._instrument_pos_y(instrument_index)
                                + event_data.register.value)),
            self,
            event_data.length,
            event_data.text,
            self.music_font)

    @staticmethod
    def _instrument_pos_y(instrument_index):
        return GridUnit(3 * instrument_index)
