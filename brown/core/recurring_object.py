from brown.utils.point import Point


class RecurringObject:

    """A mixin for GraphicObjects drawn at regular positions on every line

    All implementations of this class should implement `_render_occurence()`
    and `_render_complete()`, which may well be a passing call
    to `_render_occurrence()`.

    No other rendering methods should be overridden.
    """

    def __init__(self, line_x_percent):
        """
        Args:
            line_x_percent (float): A percentage amount for how far along
                each line this object should appear.
        """
        self.line_x_percent = line_x_percent

    ######## PRIVATE METHODS ########

    def _find_x_in_line(self, line_length):
        """Find the x location of an occurrence of the object in a line

        Args:
            line_length (Unit): The length of the line

        Returns:
            Unit: The x position of the occurrence in the line
        """
        return line_length * (self.line_x_percent / 100)

    def _render_occurence(self, pos):
        """Render an occurrence of the object at `pos`

        All RecurringObject classes should implement this.

        Args:
            pos (Point): The absolute position where this occurrence
                should appear
        """
        raise NotImplementedError

    def _render_before_break(self, local_start_x, start, stop):
        self._render_occurence(Point(start.x, start.y))

    def _render_after_break(self, local_start_x, start, stop):
        line_x = self._find_x_in_line(stop.x - start.x) + start.x
        if line_x <= stop.x:
            self._render_occurence(Point(line_x, start.y))

    def _render_spanning_continuation(self, local_start_x, start, stop):
        line_x = self._find_x_in_line(stop.x - start.x) + start.x
        self._render_occurence(Point(line_x, start.y))
