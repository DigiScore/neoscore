from brown.core.object_group import ObjectGroup
from examples.feldman_projections_2.text_event import TextEvent


class Score(ObjectGroup):

    def __init__(self, pos, content):
        super().__init__(pos)
        self.events = []

        for event in content:
            self.events.append(self.create_event(event))

    def create_event(self, content_tuple):
        pos_x = content_tuple[1]
        pos_y = content_tuple[0].vertical_offset + content_tuple[2].value
        length = content_tuple[4]
        return TextEvent((pos_x, pos_y), self, length, content_tuple[3])

