from brown.core.layout_controller import LayoutController


class LineBreak(LayoutController):
    """A line break controller."""

    def __init__(flowable_frame, x):
        super().__init__(flowable_frame, x)

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return False
