from brown.core.invisible_object import InvisibleObject


class LayoutController(InvisibleObject):
    """An abstract layout controller for working with Flowable layouts."""

    _is_automatic = False
    """bool: Whether or not this controller class is automatically created
             by its `Flowable`.
    """

    def __init__(self, pos, page, flowable_x):
        """
        Args:
            pos (Point): The position of this controller relative to its page.
            page (Page): The page this controller appears on. This is used as
                the object's parent.
            flowable_x (Unit): The position of this controller within the
                `Flowable`s local space.
        """
        super().__init__(pos, page)
        self._flowable_x = flowable_x

    ######## PUBLIC PROPERTIES ########

    @property
    def page(self):
        """Page: The page this controller appears on.

        This is identical to `self.parent`. For readability, it is encouraged
        to refer to the parent through this property.
        """
        return self.parent

    @property
    def flowable_x(self):
        """Unit: The x position in `self.flowable`s local space."""
        return self._flowable_x

    @flowable_x.setter
    def flowable_x(self, value):
        self._flowable_x = value
