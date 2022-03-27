from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Optional

from neoscore.core.positioned_object import PositionedObject
from neoscore.interface.image_interface import ImageInterface
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Image(PositionedObject):
    """An image which can be placed in the document.

    Supported image extensions/formats include: BMP, GIF, JPG, JPEG,
    PNG, PBM, PGM, PPM, XBM, XPM, and SVG.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        file_path: str | pathlib.Path,
        scale: float = 1,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent (core-level) object or None
            file_path: Path to an image file to be used
            scale: A scaling factor applied to the image.
        """
        self._scale = scale
        self.file_path = file_path
        super().__init__(pos, parent)

    @property
    def scale(self) -> float:
        """A scaling factor.

        Scaling always respects the image's aspect ratio."""
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value

    @property
    def file_path(self) -> pathlib.Path:
        """Path to an image file to be used"""
        return self._file_path

    @file_path.setter
    def file_path(self, value: str | pathlib.Path):
        if isinstance(value, str):
            value = pathlib.Path(value)
        self._file_path = value

    @property
    def breakable_length(self) -> Unit:
        """The breakable width of the object.

        This is always 0, meaning Images objects cannot be broken
        across Flowable lines.
        """
        return ZERO

    # Since Image isn't breakable (for now?), we only need to
    # implement complete rendering
    def _render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        interface = ImageInterface(pos, self.file_path, self.scale)
        interface.render()
        self.interfaces.append(interface)
