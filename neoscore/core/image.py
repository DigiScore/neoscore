from __future__ import annotations

import pathlib
from typing import Optional

from neoscore.core.layout_controllers import NewLine
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.interface.image_interface import ImageInterface


class Image(PositionedObject):
    """An image which can be placed in the document.

    Supported image extensions/formats include: BMP, GIF, JPG, JPEG,
    PNG, PBM, PGM, PPM, XBM, XPM, and SVG.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        file_path: str | pathlib.Path,
        scale: float = 1,
        rotation: float = 0,
        z_index: int = 0,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent object or None
            file_path: Path to an image file to be used
            scale: A scaling factor applied to the image.
            rotation: Rotation angle in degrees.
            z_index: Controls draw order with lower values drawn first.
        """
        self._scale = scale
        self._rotation = rotation
        self._z_index = z_index
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
    def rotation(self) -> float:
        """An angle in degrees to rotate about the image origin"""
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value

    @property
    def z_index(self) -> int:
        """Value controlling draw order with lower values being drawn first"""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int):
        self._z_index = value

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
        """The breakable length of the object.

        This is always ``ZERO``, meaning images cannot be broken across :obj:`.Flowable`
        lines.
        """
        return ZERO

    # Since Image isn't breakable (for now?), we only need to
    # implement complete rendering
    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        interface = ImageInterface(
            pos, self.file_path, self.scale, self.rotation, self.z_index
        )
        interface.render()
        self.interfaces.append(interface)
