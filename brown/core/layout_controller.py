from brown.core.invisible_object import InvisibleObject


class LayoutController(InvisibleObject):
    """An abstract layout controller for working with Flowable layouts."""

    _is_automatic = False
    """bool: Whether or not this controller class is automatically created
             by its `Flowable`.
    """

    def __init__(self, pos, page, flowable, local_x):
        """
        Args:
            pos (Point): The position of this controller relative to its page.
            page (Page): The page this controller appears on. This is used as
                the object's parent.
            flowable (Flowable): The flowable this controller
                belongs in. Note that this is *not* the object's parent.
            local_x (Unit): The position of this controller within the
                `Flowable`s local space.
        """
        super().__init__(pos, page)
        self._flowable = flowable
        self._local_x = local_x

    ######## PUBLIC PROPERTIES ########

    @property
    def page(self):
        """Page: The page this controller appears on.

        This is identical to `self.parent`. For readability, it is encouraged
        to refer to the parent through this property.
        """
        return self.parent

    @property
    def flowable(self):
        """Flowable: The parent flowable this controller is bound to."""
        return self._flowable

    @property
    def local_x(self):
        """Unit: The x position in `self.flowable`s local space."""
        return self._local_x

    @local_x.setter
    def local_x(self, value):
        self._local_x = value
