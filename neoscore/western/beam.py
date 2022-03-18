from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent

# TODO HIGH many classes are Paths with a MusicFont for getting engraving defaults and unit sizes. maybe it would make sense to make a common class for this, like MusicPath or something?


class Beam(Path, HasMusicFont):

    """A rhythmic beam connecting groups of notes.

    This is a single beam - for multiple layers of beams
    (e.g. 2 for 16th notes), multiple `Beam`s must be stacked
    on top of each other.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: Parent,
        stop: PointDef,
        stop_parent: Parent,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting (left) position of the beam
            start_parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement `HasMusicFont`.
            stop: The ending (right) position of the beam
            stop_parent: The parent for the ending position.
                Must be a staff or in one.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        Path.__init__(self, start, parent=start_parent)
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.beam_thickness = font.engraving_defaults["beamThickness"]
        # Draw beam
        stop = Point.from_def(stop)
        self.line_to(stop.x, stop.y, stop_parent)
        self.line_to(stop.x, stop.y + self.beam_thickness, stop_parent)
        self.line_to(ZERO, self.beam_thickness, self)
        self.close_subpath()

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
