from brown.core import brown
from brown.core.object_group import ObjectGroup
from brown.core.font import Font
from examples.feldman_projections_2.text_event import TextEvent
from examples.feldman_projections_2.grid_unit import GridUnit


class Score(ObjectGroup):

    _FONT_SIZE_IN_GRID_UNITS = 0.3

    def __init__(self, pos, content):
        super().__init__(pos)
        self.events = []
        self.main_font = Font.deriving(
            brown.default_font, size=GridUnit(Score._FONT_SIZE_IN_GRID_UNITS))

        for event in content:
            self.events.append(self.create_event(event))

    def create_event(self, content_tuple):
        pos_x = content_tuple[1]
        pos_y = content_tuple[0].vertical_offset + content_tuple[2].value
        length = content_tuple[4]
        return TextEvent((pos_x, pos_y), self, length, content_tuple[3],
                         self.main_font)
