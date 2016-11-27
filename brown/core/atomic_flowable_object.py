from brown.utils.point import Point
from brown.utils.units import Mm
from brown.core.flowable_object import FlowableObject


class AtomicFlowableObject(FlowableObject):

    """An abstract FlowableObject that can only be rendered complete."""

    def __init__(self, pos, frame, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            width (Unit): The drawable width of this object.
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (FlowableObject): The parent object or None.
                parents of `AtomicFlowableObject`s must all have
                the same `frame`
        """
        super().__init__(pos, 0, frame, pen, brush, parent)

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        # Inheriting subclasses should not override this, instead
        # they should override self._render_complete()
        self._render_complete

    def _render_complete(self):
        """Render the entire object.

        Inheriting subclasses must implement this to support rendering.

        Returns: None
        """
        raise NotImplementedError

    def _render_before_break(self, start, stop):
        """Inherited stub changing NotImplementedError to TypeError.

        Objects requiring cross-break rendering should not inherit
        from AtomicFlowableObject.
        """
        raise TypeError(
            'Cross-break rendering not supported by AtomicFlowableObject')

    def _render_after_break(self, start, stop):
        """Inherited stub changing NotImplementedError to TypeError.

        Objects requiring cross-break rendering should not inherit
        from AtomicFlowableObject.
        """
        raise TypeError(
            'Cross-break rendering not supported by AtomicFlowableObject')

    def _render_spanning_continuation(self, start, stop):
        """Inherited stub changing NotImplementedError to TypeError.

        Objects requiring cross-break rendering should not inherit
        from AtomicFlowableObject.
        """
        raise TypeError(
            'Cross-break rendering not supported by AtomicFlowableObject')

    # TODO: Maybe self.width should be overridden somehow so that
    #       it is clear that it doesn't apply to this class?
