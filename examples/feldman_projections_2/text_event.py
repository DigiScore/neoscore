from brown.core.text import Text
from brown.utils.point import Point
from examples.feldman_projections_2.event import Event
from examples.feldman_projections_2.grid_unit import GridUnit


class TextEvent(Event):

    def __init__(self, pos, parent, length, text, font):
        Event.__init__(self, pos, parent, length)
        text_pos = TextEvent._calculate_text_pos(text, font)
        self.text = Text(text_pos, text, font, self)

    @staticmethod
    def _calculate_text_pos(text, font):
        text_rect = font.bounding_rect_of(text)
        x = (GridUnit(1) - text_rect.width) / 2
        y = GridUnit(1) - ((GridUnit(1) - text_rect.height) / 2)
        return Point(x, y)
