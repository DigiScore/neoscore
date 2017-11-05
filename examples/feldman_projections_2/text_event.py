from brown.core.text import Text
from examples.feldman_projections_2.event import Event


class TextEvent(Event):

    def __init__(self, pos, parent, length, text):

        Event.__init__(self, pos, parent, length)
        self.text = Text(pos, text, parent=self)
