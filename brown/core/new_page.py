from brown.core.new_line import NewLine
from brown.utils.units import Mm


class NewPage(NewLine):
    """A line break controller."""

    def __init__(self, flowable_frame, x, page_number, page_pos, offset_y=0):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (float): The x position in pixels in the frame's local space.
            offset_y (float): The space in pixels above the first
                line on the next page.
        """
        if not offset_y:
            offset_y = Mm(0)
        super().__init__(flowable_frame, x, page_number, page_pos, offset_y)

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self):
        """float: The space in pixels above the first line on the next page."""
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value
