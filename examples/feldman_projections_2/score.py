from brown import config
from brown.core import brown
from brown.core.music_font import MusicFont
from brown.core.object_group import ObjectGroup
from brown.core.font import Font
from brown.core.staff import Staff
from brown.utils.units import GraphicUnit
from examples.feldman_projections_2.glyph_name import GlyphName
from examples.feldman_projections_2.text_event import TextEvent
from examples.feldman_projections_2.grid_unit import GridUnit


class Score(ObjectGroup):

    _TEXT_FONT_SIZE = GraphicUnit(GridUnit(0.8)).value
    _MUSIC_FONT_SIZE = Staff._make_unit_class(GridUnit(0.8))

    def __init__(self, pos, content):
        super().__init__(pos)
        self.events = []
        self.text_font = Font.deriving(
            brown.default_font,
            size=Score._TEXT_FONT_SIZE)
        self.music_font = MusicFont(
            config.DEFAULT_MUSIC_FONT_NAME,
            Score._MUSIC_FONT_SIZE)

        for event in content:
            self.events.append(self.create_event(event))

    def create_event(self, content_tuple):
        pos_x = content_tuple[1]
        pos_y = content_tuple[0].vertical_offset + content_tuple[2].value
        length = content_tuple[4]
        text = content_tuple[3]
        font = (self.music_font if isinstance(text, GlyphName)
                else self.text_font)
        return TextEvent((pos_x, pos_y), self, length, content_tuple[3],
                         font)
