from brown.core.horizontal_spanner import HorizontalSpanner
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject
from brown.utils.units import Unit


class PedalLine(HorizontalSpanner, Path, StaffObject):

    """A line-style pedal marking with optional half-lift (^) marks.

    The mark begins with an upward crook, continues as a horizontal
    line interrupted with optional half-lift upward triangular marks,
    and terminates with another upward crook.

    The object's position is that of the top of the opening crook;
    this y-axis position is also the height two which the half-lift
    marks extend. The main line of the path is drawn 1 staff unit
    below this position.

    A list of half-lift x-axis positions may be provided as either
    simple x-axis Unit values (relative to the line's start position)
    or as 2-tuples of x-axis positions and position parents:

    >>> PedalLine(start=(Mm(10), staff.unit(8)), start_parent=staff,
    ...           end_x=Mm(200), end_parent=None,
    ...           half_lift_positions=[
    ...               Mm(20),               # Relative to start_parent
    ...               Mm(40),               # Relative to start_parent
    ...               (Mm(1), some_chord)]  # 1 mm right of some_chord
    ...          ) # doctest: +SKIP

    """

    def __init__(self,
                 start, start_parent,
                 end_x, end_parent=None,
                 half_lift_positions=None):
        """
        Args:
            start (Point or init tuple): The starting position of the
                pedal line.
            start_parent (GraphicObject): An object either in a Staff
                or an actual Staff.
            end_x (Unit): The
        """
        StaffObject.__init__(self, start_parent)
        pen = Pen(thickness=self.staff.music_font.engraving_defaults[
            'pedalLineThickness'])
        Path.__init__(self, start, pen, parent=start_parent)
        HorizontalSpanner.__init__(self, end_x, end_parent)
        self.half_lift_positions = half_lift_positions
        self._draw_path()

    ######## PRIVATE METHODS ########

    def _draw_path(self):
        """Draw the path according to this object's attributes.

        Returns: None
        """
        # Set up constants
        # The vertical extent of the shape
        descent = self.staff.unit(1)
        # The horizontal distance extended to from half lift positions
        half_lift_x_extent = self.staff.unit(0.5)

        # Draw opening crook
        self.line_to(self.staff.unit(0), descent)

        # Draw half lift positions, if any exist
        for pos in self.half_lift_positions:
            if isinstance(pos, tuple):
                lift_parent = pos[1]
                lift_center_x = pos[0]
                if self.flowable is not None:
                    lift_center_y = self.flowable.map_between_locally(
                        lift_parent, self).y + descent
            elif isinstance(pos, Unit):
                lift_parent = self
                lift_center_x = pos
                lift_center_y = descent
            else:
                raise AttributeError(
                    'Invalid half lift position: {}'.format(pos))
            lift_left_x = lift_center_x - half_lift_x_extent
            lift_right_x = lift_center_x + half_lift_x_extent
            self.line_to(lift_left_x, lift_center_y, lift_parent)
            self.line_to(lift_center_x, lift_center_y - descent, lift_parent)
            self.line_to(lift_right_x, lift_center_y, lift_parent)

        # Draw closing crook
        self.line_to(self.end_x, self.end_y + descent, self.end_parent)
        self.line_to(self.end_x, self.end_y, self.end_parent)
