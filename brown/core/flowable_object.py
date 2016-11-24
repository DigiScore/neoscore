from brown.core.flowable_frame import FlowableFrame
from brown.core.graphic_object import GraphicObject



class FlowableObject(GraphicObject):

    @property
    def flowable(self):
        return self._flowable

    @flowable.setter
    def flowable(self, value):
        self._flowable = value

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        # TODO: Break object into horizontal sections and make calls
        #       to the private rendering methods.
        raise NotImplementedError

    ######## PRIVATE METHODS ########

    def _render_complete(self):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_before_break(self, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_after_break(self, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_spanning_continuation(self, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that
        crosses two breaks. This function should render the
        portion of the object surrounded by breaks on either side.

        Args:
            start (Point): The starting point for drawing.
            stop (Point): The stopping point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError
