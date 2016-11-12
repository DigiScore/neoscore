from abc import ABC


class LayoutController(ABC):
    """
    An abstract layout controller for working with FlowableFrame layouts.
    """

    def __init__(self, flowable_frame, x):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (float): The x position in pixels in the frame's local space.
        """
        self._flowable_frame = flowable_frame
        self._x = x

    ######## PUBLIC PROPERTIES ########

    @property
    def flowable_frame(self):
        """FlowableFrame: The parent frame this controller is bound to."""
        return self._flowable_frame

    @flowable_frame.setter
    def flowable_frame(self, value):
        self._flowable_frame = value

    @property
    def x(self):
        """float: The x position in the parent FlowableFrame's local space."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        """bool: Whether or not this controller was created automatically.

        This property is read-only.
        """
        raise NotImplementedError
