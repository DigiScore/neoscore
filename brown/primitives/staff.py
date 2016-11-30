from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.config import config
from brown.primitives.clef import Clef
from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject


class Staff(GraphicObject):
    """A staff capable of holding `StaffObject`s"""

    def __init__(self, pos, width, frame, staff_unit=None, line_count=5):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            width (Unit): The horizontal width of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to config.DEFAULT_STAFF_UNIT
            line_count (int): The number of lines in the staff.
        """
        self._interface = PathInterface(pos)
        super().__init__(pos, width, parent=frame)
        self._line_count = line_count
        self._width = width
        if staff_unit:
            self.staff_unit = staff_unit
        else:
            self.staff_unit = config.DEFAULT_STAFF_UNIT
        self._contents = []

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self):
        """GraphicUnit: The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.

        This property is read-only.
        """
        return (self.line_count - 1) * self.staff_unit

    @property
    def line_count(self):
        """int: The number of lines in the staff

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._line_count

    @property
    def contents(self):
        """list[StaffObject]: A list of staff objects belonging to the staff

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._contents

    @property
    def highest_position(self):
        """int: The staff position of the top line

        This property is read-only
        """
        return self.line_count - 1

    @property
    def lowest_position(self):
        """int: The staff position of the bottom line

        This property is read-only.
        """
        return (self.line_count - 1) * -1

    ######## PUBLIC METHODS ########

    def active_clef_at(self, position_x):
        """Find and return the active clef at a given point.

        Returns: Clef
        """
        # TODO: Find a more efficient way to quickly look up contents by type
        clefs_before = [item for item in self.contents
                        if isinstance(item, Clef) and
                        item.position_x <= position_x]
        return max(clefs_before, key=lambda c: c.position_x, default=None)

    def middle_c_at(self, position_x):
        """Find the vertical staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c. If no clef is present, treble is assumed.

        Returns:
            int: A vertical staff position, where 0 means the center
            line or space of the staff, higher numbers mean higher positions,
            and lower numbers mean lower positions.
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            # Assume treble
            return Clef._middle_c_staff_positions['treble']
        else:
            return clef.middle_c_staff_position

    def _natural_midi_number_of_top_line_at(self, position_x):
        """Find the natural midi pitch class of the top line at a given point.

        Looks for clefs and other transposing modifiers to determine
        the this value. If no clef is present, treble is assumed.

        Returns an `int` midi pitch number.
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            # Assume treble
            return Clef._natural_midi_numbers_at_top_staff_line['treble']
        else:
            return clef._natural_midi_number_at_top_staff_line

    ######## PRIVATE METHODS ########

    def _draw_staff_span(self, start, length):
        """Draw a section of the staff in the given path.

        This is a helper method for the rendering methods.

        Args:
            start (Point): The starting doc-space point for drawing.
            stop (Point): The stopping doc-space point for drawing.

        Returns: None"""
        for i in range(self.line_count):
            y_offset = self.staff_unit * i
            self._interface.move_to(Point(GraphicUnit(0), y_offset) + start)
            self._interface.line_to(Point(length, y_offset) + start)

    def _render_complete(self):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        # Draw the staff lines
        print('rendering complete')
        self._draw_staff_span(self.pos, self.width)

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
        self._draw_staff_span(start, delta.x)

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
        self._draw_staff_span(start, delta.x)

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
        self._draw_staff_span(start, delta.x)

    def _staff_pos_to_top_down(self, centered_value):
        """Convert a staff position to its top-down equivalent.

        This takes a centered staff position (where 0 means the center
        position positive values mean higher positions, and lower values
        vice versa) and returns its equivalent in the top-down system
        (where 0 means the top line of the staff, negative values
        extend upward, and positive values extend downward).

        This is mostly meant for internal purposes in the rendering
        pipeline. Values should not be stored in objects as these values.

        Args:
            centered_value (int): A staff position in the centered system.

        Returns:
            int: A staff position in the top-down system

        Example:
            # TODO: Make me
        """
        return (-1 * centered_value) + self.line_count - 1

    def _staff_pos_to_rel_pixels(self, staff_position):
        """Convert a staff position to pixels relative to the staff.

        This takes a centered staff position (where 0 means the center
        position positive values mean higher positions, and lower values
        vice versa) and returns its translation to pixels relative to the
        top of the staff, where 0 is the top of the staff, negative values
        extend upward, and positive values extend downward

        Args:
            centered_value (float): A staff position in the centered system.

        Returns:
            float: A y-axis pixel position relative to the top of the staff

        Example:
            # TODO: Make me
        """
        return ((self.staff_unit / 2) *
                self._staff_pos_to_top_down(staff_position))

    # TODO: Implement more functions breaking apart the translation of staff
    #       space to flowable space.

    def _position_inside_staff(self, position):
        """bool: Determine if a position is inside the staff.

        This is true for any position within or on the outer lines.
        """
        return self.lowest_position <= position <= self.highest_position

    def _position_outside_staff(self, position):
        """bool: Determine if a position is outside of the staff.

        This is true for any position not on or between the outer staff lines.
        """
        return not self._position_inside_staff(position)

    def _position_on_ledger(self, position):
        """bool: Tell if a position is on a ledger line position"""
        # If the position is outside the staff and self.count_count and
        # position's evenness are different, a ledger line is needed
        return (self._position_outside_staff(position) and
                self.line_count % 2 != position % 2)

    def _ledgers_needed_from_position(self, position):
        """set{int}: Ledgers needed for a note at a given position."""
        direction = 1 if position < 0 else -1
        if position is None or self._position_inside_staff(position):
            return set()
        else:
            # Find start and end points for ledger generation
            start = position
            if not self._position_on_ledger(position):
                start += direction
            if direction == 1:
                end = self.lowest_position
            else:
                end = self.highest_position
            return {pos for pos in range(start, end, 2 * direction)}

    def _register_staff_object(self, staff_object):
        """Add a StaffObject to `self.contents`.

        Args:
            staff_object (StaffObject): The object to add to `self.contents`

        Warning:
            This does not set `staff_object.staff` to self"""
        self._contents.append(staff_object)
        staff_object.staff = self
