from brown.core.text import Text
from examples.feldman_projections_2.event import Event
from examples.feldman_projections_2.grid_unit import GridUnit


class TextEvent(Event):

    def __init__(self, pos, parent, length, text):

        Event.__init__(self, pos, parent, length)
        self.text = Text((GridUnit(0), GridUnit(0)), text, parent=self)
