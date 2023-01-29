from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import PenDef
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject


class MusicPath(Path, HasMusicFont):
    """A Path with a music font.

    This is mostly useful as a superclass for paths which use a
    MusicFont's engraving defaults and staff unit to control their
    appearance, but it can also be instantiated directly.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        rotation: float = 0,
        background_brush: Optional[BrushDef] = None,
        transform_origin: PointDef = ORIGIN,
    ):
        """
        Args:
            pos: The position of the path root.
            parent: The parent object. If no font is given, this or one of its
                ancestors must implement ``HasMusicFont``.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
            rotation: Angle in degrees. Rotated paths with flowable breaks and
                path elements anchored to other objects are not currently supported.
            background_brush: Optional brush used to paint the path's bounding rect
                behind it.
            transform_origin: The origin point for rotation and scaling transforms
        """
        Path.__init__(
            self,
            pos,
            parent,
            brush,
            pen,
            rotation,
            background_brush,
            transform_origin,
        )
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
