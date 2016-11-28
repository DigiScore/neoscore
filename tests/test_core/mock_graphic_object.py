from brown.utils.units import Mm
from brown.interface.invisible_object_interface import InvisibleObjectInterface
from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject


class MockGraphicObject(GraphicObject):

    """A mock GraphicObject subclass mostly for testing parentage."""

    _interface_class = PathInterface

    def __init__(self, pos, breakable_width=0,
                 pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            parent: The parent (core-level) object or None
        """
        self._interface = type(self)._interface_class(pos)
        super().__init__(pos=pos, breakable_width=breakable_width,
                         pen=pen, brush=brush, parent=parent)
        # TEMPORARY if/else while document_pos isn't fully implemented
        if self.is_in_flowable:
            self._interface.pos = self.document_pos
        else:
            self._interface.pos = self.pos

    def _draw_mock_staff_line(self, path, start, length):
        for i in range(4):
            y_offset = Mm(1) * i
            path.move_to((0, y_offset) + start)
            path.line_to((length, y_offset) + start)

    def _render_complete(self):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        self._draw_mock_staff_line(self._interface, self.pos, self.width)

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
        delta = stop - start
        self._draw_mock_staff_line(self._interface, start, delta.x)

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
        delta = stop - start
        self._draw_mock_staff_line(self._interface, start, delta.x)

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
        delta = stop - start
        self._draw_mock_staff_line(self._interface, start, delta.x)
