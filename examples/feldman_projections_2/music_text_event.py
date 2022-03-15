from examples.feldman_projections_2.event import Event
from examples.feldman_projections_2.grid_unit import GridUnit
from neoscore.core.music_text import MusicText
from neoscore.utils.point import Point


class MusicTextEvent(Event):

    _STEM_OFFSET_GRID_UNITS = 0.02

    def __init__(self, pos, parent, length, text, font):
        Event.__init__(self, pos, parent, length)
        self.text = MusicText(pos, self, text, font)
        MusicTextEvent._center_music_text(self.text)

    @staticmethod
    def _center_music_text(music_text):
        text_rect = music_text.bounding_rect
        x = (GridUnit(1 - MusicTextEvent._STEM_OFFSET_GRID_UNITS) - text_rect.width) / 2
        y = GridUnit(0.5)
        music_text.pos = Point(x, y)
