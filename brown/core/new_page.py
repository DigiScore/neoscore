from brown.core.layout_controller import LayoutController
from brown.utils.mm import Mm


class NewPage(LayoutController):
    """A line break controller."""

    def __init__(self, flowable_frame, x, offset_y=0):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (float): The x position in pixels in the frame's local space.
            offset_y (float): The space in pixels above the first
                line on the next page.
        """
        super().__init__(flowable_frame, x)
        self.offset_y = offset_y if offset_y else Mm(0)

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self):
        """
        (float): The space in pixels above the first line on the next page.
        """
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return False
