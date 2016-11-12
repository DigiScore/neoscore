from brown.core.layout_controller import LayoutController


class LineBreak(LayoutController):
    """A line break controller."""

    def __init__(self, flowable_frame, x, margin_above_next=None):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (float): The x position in pixels in the frame's local space.
            margin_above_next (float): The space between the bottom of the
                current line and the top of the next, in pixels.
        """
        super().__init__(flowable_frame, x)
        self.margin_above_next = margin_above_next

    ######## PUBLIC PROPERTIES ########

    @property
    def margin_above_next(self):
        """float: The space in pixels before the next line."""
        return self._margin_above_next

    @margin_above_next.setter
    def margin_above_next(self, value):
        self._margin_above_next = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return False
