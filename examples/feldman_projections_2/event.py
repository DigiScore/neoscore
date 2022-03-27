from examples.feldman_projections_2.grid_unit import GridUnit
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner


class Event(PositionedObject, Spanner):
    """An abstract boxed event."""

    def __init__(self, pos, parent, length):
        PositionedObject.__init__(self, pos, parent)
        Spanner.__init__(self, length, self)
        self.event_box = _EventBox(self, self.spanner_x_length)


class _EventBox(Path, Spanner):

    box_pen = Pen(thickness=GridUnit(0.07), join_style=PenJoinStyle.MITER)

    def __init__(self, parent, length):
        Path.__init__(
            self, (GridUnit(0), GridUnit(0)), parent=parent, pen=_EventBox.box_pen
        )
        Spanner.__init__(self, length, self)
        self._construct_path()

    def _construct_path(self):
        self.line_to(self.end_x, GridUnit(0))
        self.line_to(self.end_x, GridUnit(1))
        self.line_to(GridUnit(0), GridUnit(1))
        self.line_to(GridUnit(0), GridUnit(0))
        self.close_subpath()
