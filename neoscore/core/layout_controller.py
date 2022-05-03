from neoscore.core.units import Unit


class LayoutController:
    """An abstract layout controller for working with Flowable layouts."""

    def __init__(self, flowable_x: Unit):
        """
        Args:
            flowable_x: The position of this controller within the owning
                flowable's local space.
        """
        self._flowable_x = flowable_x

    ######## PUBLIC PROPERTIES ########

    @property
    def flowable_x(self) -> Unit:
        """The x position in the flowable's local space."""
        return self._flowable_x

    @flowable_x.setter
    def flowable_x(self, value: Unit):
        self._flowable_x = value
