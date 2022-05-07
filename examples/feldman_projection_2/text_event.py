from examples.feldman_projection_2.event import Event
from examples.feldman_projection_2.grid_unit import GridUnit
from neoscore.core.text import Text
from neoscore.core.text_alignment import AlignmentX, AlignmentY


class TextEvent(Event):

    """An Event box with a plaintext Text object inside it."""

    def __init__(self, pos, parent, length, text, font):
        Event.__init__(self, pos, parent, length)
        self.text = Text(
            (GridUnit(0.5), GridUnit(0.5)),
            self,
            text,
            font,
            alignment_x=AlignmentX.CENTER,
            alignment_y=AlignmentY.CENTER,
        )
