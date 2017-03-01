from brown.core.new_line import NewLine
from brown.utils.units import Mm


class NewPage(NewLine):
    """A new line that starts a new page."""

    def __init__(self, flowable_frame, x, pos, offset_y=None):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (Unit): The x position in the frame's local space where this
                page begins.
            pos (Point): The position of the top left corner of this line.
            offset_y (Unit): The space between the bottom of the
                current line and the top of the next.
        """
        if not offset_y:
            offset_y = Mm(0)
        super().__init__(flowable_frame, x, pos, offset_y)

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self):
        """Unit: The space above the first line on the next page."""
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value
