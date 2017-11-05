from brown.core.object_group import ObjectGroup
from brown.core.horizontal_spanner import HorizontalSpanner
from brown.core.path import Path
from examples.feldman_projections_2.grid_unit import GridUnit


class Event(ObjectGroup, HorizontalSpanner):
    """An abstract boxed event."""

    def __init__(self, pos, parent, length):
        ObjectGroup.__init__(self, pos, parent)
        HorizontalSpanner.__init__(self, pos.x + length)
        self.event_box = _EventBox(pos, self, self.spanner_x_length)


class _EventBox(Path, HorizontalSpanner):

    def __init__(self, pos, parent, length):
        Path.__init__(self, pos, parent=parent)
        HorizontalSpanner.__init__(self, pos.x + length)

    def _construct_path(self):
        self.line_to(self.end_x, GridUnit(0))
        self.line_to(self.end_x, GridUnit(1))
        self.line_to(GridUnit(0), GridUnit(1))
        self.line_to(GridUnit(0), GridUnit(0))
        self.close_subpath()
