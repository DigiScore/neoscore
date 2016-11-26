from brown.core.flowable_object import FlowableObject
from brown.interface.path_interface import PathInterface
from brown.utils.point import Point


class MockFlowableObject(FlowableObject):

    """A mock concrete FlowableObject for testing"""

    def _render_complete(self):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        line = PathInterface(self.document_pos, self.pen, self.brush, self.parent)
        line.line_to((self.width, 0))
        line.render()
        self._interfaces.append(line)

    def _render_before_break(self, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        Args:
            start (Point): The starting doc-space point for drawing.
            stop (Point): The stopping doc-space point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        line = PathInterface(start, '#ff0000', self.brush, self.parent)
        delta = stop - start
        line.line_to(delta)
        line.render()
        self._interfaces.append(line)

    def _render_after_break(self, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        Args:
            start (Point): The starting doc-space point for drawing.
            stop (Point): The stopping doc-space point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        line = PathInterface(start, '#00ff00', self.brush, self.parent)
        delta = stop - start
        line.line_to(delta)
        line.render()
        self._interfaces.append(line)

    def _render_spanning_continuation(self, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that
        crosses two breaks. This function should render the
        portion of the object surrounded by breaks on either side.

        Args:
            start (Point): The starting doc-space point for drawing.
            stop (Point): The stopping doc-space point for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        line = PathInterface(start, '#0000ff', self.brush, self.parent)
        delta = stop - start
        line.line_to(delta)
        line.render()
        self._interfaces.append(line)
