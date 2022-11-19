from __future__ import annotations

from typing import Optional

from neoscore.core.brush import Brush
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.core.units import Unit


class PedalLine(Spanner, MusicPath):

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

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: PositionedObject,
        end_x: Unit,
        end_parent: Optional[PositionedObject] = None,
        half_lift_positions: List[Unit | Tuple[Unit, PositionedObject]] = None,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting position of the pedal line.
            start_parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement ``HasMusicFont``.
            end_x: x position of the end point relative to end_parent
            end_parent: parent for end_x
            half_lift_positions: A list of x-axis positions along the line
                where half lift notches should be drawn.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicPath.__init__(self, start, start_parent, font, Brush.no_brush(), Pen())
        self.pen.thickness = self.music_font.engraving_defaults["pedalLineThickness"]
        Spanner.__init__(self, end_x, end_parent or self)
        self.half_lift_positions = half_lift_positions
        self._draw_path()

    def _draw_path(self):
        """Draw the path according to this object's attributes.

        Returns: None
        """
        # Set up constants
        # The vertical extent of the shape
        descent = self.music_font.unit(1)
        # The horizontal distance extended to from half lift positions
        half_lift_x_extent = self.music_font.unit(0.5)

        # Draw opening crook
        self.line_to(self.music_font.unit(0), descent)

        # Draw half lift positions, if any exist
        if self.half_lift_positions:
            for pos in self.half_lift_positions:
                if pos >= self.end_x - (half_lift_x_extent * 2):
                    raise AttributeError("Invalid half lift position: {}".format(pos))
                if isinstance(pos, tuple):
                    lift_parent = pos[1]
                    lift_center_x = pos[0]
                    lift_center_y = lift_parent.map_to(self).y + descent
                elif isinstance(pos, Unit):
                    lift_parent = self
                    lift_center_x = pos
                    lift_center_y = descent
                else:
                    raise AttributeError("Invalid half lift position: {}".format(pos))
                lift_left_x = lift_center_x - half_lift_x_extent
                lift_right_x = lift_center_x + half_lift_x_extent
                self.line_to(lift_left_x, lift_center_y, lift_parent)
                self.line_to(lift_center_x, lift_center_y - descent, lift_parent)
                self.line_to(lift_right_x, lift_center_y, lift_parent)

        # Draw closing crook
        self.line_to(self.end_x, self.end_y + descent, self.end_parent)
        self.line_to(self.end_x, self.end_y, self.end_parent)
