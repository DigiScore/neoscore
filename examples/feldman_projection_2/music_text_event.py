from examples.feldman_projection_2.event import Event
from examples.feldman_projection_2.grid_unit import GridUnit
from neoscore.core.music_text import MusicText
from neoscore.core.text_alignment import AlignmentX, AlignmentY


class MusicTextEvent(Event):

    """An Event box with a MusicText glyph inside it"""

    def __init__(self, pos, parent, length, text, font):
        Event.__init__(self, pos, parent, length)
        self.text = MusicText(
            (GridUnit(0.5), GridUnit(0.5)),
            self,
            text,
            font,
            alignment_x=AlignmentX.CENTER,
            alignment_y=AlignmentY.CENTER,
        )
