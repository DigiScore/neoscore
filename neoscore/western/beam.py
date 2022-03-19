from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.brush import SimpleBrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import SimplePenDef
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


# TODO MEDIUM normalize "end" vs "stop" in spanner-like args


class Beam(MusicPath):

    """A rhythmic beam connecting groups of notes.

    This is a single beam - for multiple layers of beams
    (e.g. 2 for 16th notes), multiple `Beam`s must be stacked
    on top of each other.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Parent,
        end_pos: PointDef,
        end_parent: Parent,
        font: Optional[MusicFont] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """
        Args:
            pos: The starting (left) position of the beam
            parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement `HasMusicFont`.
            end_pos: The ending (right) position of the beam
            end_parent: The parent for the ending position.
                Must be a staff or in one.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        MusicPath.__init__(self, pos, parent, font, brush, pen)
        self.beam_thickness = self.music_font.engraving_defaults["beamThickness"]
        # Draw beam
        end_pos = Point.from_def(end_pos)
        self.line_to(end_pos.x, end_pos.y, end_parent)
        self.line_to(end_pos.x, end_pos.y + self.beam_thickness, end_parent)
        self.line_to(ZERO, self.beam_thickness, self)
        self.close_subpath()
