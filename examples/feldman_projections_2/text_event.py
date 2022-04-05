from examples.feldman_projections_2.event import Event
from examples.feldman_projections_2.grid_unit import GridUnit
from neoscore.core.point import Point
from neoscore.core.text import Text


class TextEvent(Event):
    def __init__(self, pos, parent, length, text, font):
        Event.__init__(self, pos, parent, length)
        text_pos = TextEvent._calculate_text_pos(text, font)
        self.text = Text(text_pos, self, text, font)

    @staticmethod
    def _calculate_text_pos(text, font):
        text_rect = font.bounding_rect_of(text)
        x = (GridUnit(1) - text_rect.width) / 2
        y = GridUnit(1) - ((GridUnit(1) - text_rect.height) / 2)
        return Point(x, y)
