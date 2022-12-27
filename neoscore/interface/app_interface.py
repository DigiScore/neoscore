from __future__ import annotations

import multiprocessing
import pathlib
import threading
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple

from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, QPoint, QRectF
from PyQt5.QtGui import (
    QBitmap,
    QColor,
    QFontDatabase,
    QImage,
    QPainter,
    QPixmapCache,
    QRegion,
)
from PyQt5.QtWidgets import QApplication, QGraphicsScene

from neoscore.core import env, math_helpers
from neoscore.core.color import Color
from neoscore.core.exceptions import FontRegistrationError, ImageExportError
from neoscore.core.key_event import KeyEvent
from neoscore.core.mouse_event import MouseEvent
from neoscore.core.point import Point
from neoscore.core.propagating_thread import PropagatingThread
from neoscore.core.rect import Rect, RectDef
from neoscore.core.units import Inch, Mm
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.qt import file_paths
from neoscore.interface.qt.converters import (
    color_to_q_color,
    qt_point_to_point,
    rect_to_qt_rect_f,
)
from neoscore.interface.qt.main_window import MainWindow
from neoscore.interface.qt.viewport import Viewport
from neoscore.interface.repl import running_in_ipython_gui_repl

if TYPE_CHECKING:
    from neoscore.core.document import Document

_RENDER_IMAGE_THREAD_MAX = multiprocessing.cpu_count()
_INCHES_PER_METER: float = Inch(1) / Mm(1000)
_QT_PIXMAP_CACHE_LIMIT_KB = 200_000


class AppInterface:
    """The primary interface to the application state.

    This holds much of the global application state. An ``AppInterface`` must be created
    near the start of neoscore programs.
    """

    _QT_FONT_ERROR_CODE = -1

    def __init__(
        self,
        document: Document,
        repl_refresh_func: Callable[[float], float],
        background_brush: BrushInterface,
        auto_viewport_interaction_enabled: bool,
    ):
        self.document = document
        args = ["TestApplication", "-platform", "offscreen"] if env.HEADLESS else []
        self.app = QApplication(args)
        self.main_window = MainWindow()
        self.scene = QGraphicsScene()
        self.view: Viewport = self.main_window.graphicsView
        self.view.setScene(self.scene)
        self.background_brush = background_brush
        self.auto_viewport_interaction_enabled = auto_viewport_interaction_enabled
        self.font_database = QFontDatabase()
        self.repl_refresh_func = repl_refresh_func
        self.render_image_thread_semaphore = threading.Semaphore(
            _RENDER_IMAGE_THREAD_MAX
        )
        self._viewport_rotation = 0

    def set_refresh_func(self, refresh_func: Callable[[float], float]):
        """Set a function to run automatically on a timer in the main window."""
        self.main_window.refresh_func = refresh_func

    def set_mouse_event_handler(self, handler: Callable[[MouseEvent], None]):
        """Set a function to run on mouse events."""
        self.main_window.graphicsView.mouse_event_handler = handler

    def set_key_event_handler(self, handler: Callable[[KeyEvent], None]):
        """Set a function to run on keyboard input events."""
        self.main_window.graphicsView.key_event_handler = handler

    def show(
        self,
        min_size: Optional[Tuple[int, int]] = None,
        max_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
    ):
        """Open a window showing a preview of the document.

        Args:
            min_size: An optional ``(width, height)`` minimum window size tuple.
            max_size: An optional ``(width, height)`` maximum window size tuple.
            fullscreen: Whether to show the window in fullscreen mode.
                This doesn't mix well with ``max_window_size``.
        """
        self._optimize_for_interactive_view()
        self.main_window.show(min_size, max_size, fullscreen)
        if running_in_ipython_gui_repl():
            # Do not run app.exec_() in GUI REPL mode, since IPython
            # manages the GUI thread in that case.
            if not self.main_window.refresh_func:
                self.main_window.refresh_func = self.repl_refresh_func
        else:
            self.app.exec_()

    def render_image(
        self,
        rect: Optional[RectDef],
        dest: str | pathlib.Path | bytearray,
        dpi: int,
        quality: int,
        bg_color: Color,
        autocrop: bool,
        preserve_alpha: bool,
    ) -> PropagatingThread:
        """Render the scene, or part of it, to a saved image.

        This renders on the main thread but autocrops and saves the image
        on a spawned thread which is returned to allow efficient rendering
        of many images in parallel. ``render_image`` will block if too many
        render threads are already running.

        Args:
            rect: The part of the document to render, in document coordinates.
                If ``None``, the entire scene will be rendered.
            dest: An output file path or a bytearray to save to. If a bytearray
                is given, the output format will be PNG.
            dpi: The pixels per inch of the rendered image.
            quality: The quality of the output image for compressed
                image formats. Must be either ``-1`` (default compression) or
                between ``0`` (most compressed) and ``100`` (least compressed).
            bg_color: The background color for the image.
            autocrop: Whether to crop the output image to tightly
                fit the contents of the frame. If true, the image will be
                cropped such that all 4 edges have at least one pixel not of
                ``bg_color``.
            preserve_alpha: Whether to preserve the alpha channel. If false,
                some non-transparent ``bg_color`` should be provided.

        Raises:
            ImageExportError: If Qt image export fails for unknown reasons.

        """
        dpm = AppInterface._dpi_to_dpm(dpi)
        scale = dpm / Mm(1000).base_value
        if rect:
            source_rect = rect_to_qt_rect_f(Rect.from_def(rect))
        else:
            source_rect = self.scene.sceneRect()
        pix_width = int(source_rect.width() * scale)
        pix_height = int(source_rect.height() * scale)

        if preserve_alpha:
            q_image_format = QImage.Format_ARGB32
        else:
            q_image_format = QImage.Format_RGB32

        q_image = QImage(pix_width, pix_height, q_image_format)
        q_image.setDotsPerMeterX(dpm)
        q_image.setDotsPerMeterY(dpm)
        q_color = color_to_q_color(bg_color)
        q_image.fill(q_color)

        painter = QPainter()
        painter.begin(q_image)
        painter.setRenderHint(QPainter.Antialiasing)

        target_rect = QRectF(q_image.rect())

        self.scene.render(painter, target=target_rect, source=source_rect)
        painter.end()

        def finalize():
            with self.render_image_thread_semaphore:
                final_image = (
                    AppInterface._autocrop(q_image, q_color) if autocrop else q_image
                )
                if isinstance(dest, bytearray):
                    output_array = QByteArray()
                    qbuf = QBuffer(output_array)
                    qbuf.open(QIODevice.OpenModeFlag.WriteOnly)
                    success = final_image.save(qbuf, quality=quality, format="PNG")
                    qbuf.close()
                    dest.clear()
                    dest.extend(output_array)
                else:
                    success = final_image.save(
                        file_paths.resolve_qt_path(dest), quality=quality
                    )
                if not success:
                    dest_description = (
                        "bytearray" if isinstance(dest, bytearray) else dest
                    )
                    raise ImageExportError(
                        "Unknown error occurred when exporting image to "
                        + dest_description
                    )

        thread = PropagatingThread(target=finalize)
        thread.start()
        return thread

    def destroy(self):
        """Destroy the window and all global interface-level data."""
        self.app.exit()
        self.app = None
        self.scene = None

    def register_font(self, font_file_path: str | pathlib.Path) -> List[str]:
        """Register a font file with the graphics engine.

        Args:
            font_file_path: A path to a font file. Supports TrueType and OpenType formats.

        Returns:
            A list of font families found in the font.

        Raises:
            FontRegistrationError:
                If the registration fails for any reason.
        """
        font_file_path = file_paths.resolve_qt_path(font_file_path)
        font_id = self.font_database.addApplicationFont(font_file_path)
        if font_id == AppInterface._QT_FONT_ERROR_CODE:
            raise FontRegistrationError(font_file_path)
        family_names = self.font_database.applicationFontFamilies(font_id)
        if not len(family_names):
            # I think this should be impossible, but log a warning just in case
            print(f"Warning: font at {font_file_path} provided no family names")
        return self.font_database.applicationFontFamilies(font_id)

    @property
    def background_brush(self) -> BrushInterface:
        """The brush used to paint the scene background"""
        return self._background_brush

    @background_brush.setter
    def background_brush(self, value: BrushInterface):
        self._background_brush = value
        self.scene.setBackgroundBrush(value.qt_object)

    @property
    def auto_viewport_interaction_enabled(self) -> bool:
        """Whether mouse and scrollbar viewport interaction is enabled"""
        return self._auto_viewport_interaction_enabled

    @auto_viewport_interaction_enabled.setter
    def auto_viewport_interaction_enabled(self, value: bool):
        self._auto_viewport_interaction_enabled = value
        self.view.set_auto_interaction(value)

    @property
    def viewport_center_pos(self) -> Point:
        """The interactive viewport's center position in document space."""
        # Working out the center position from the transform matrix and window
        # dimensions is pretty tricky, so hand the job to Qt.
        return qt_point_to_point(self.view.mapToScene(self.view.rect().center()))

    @viewport_center_pos.setter
    def viewport_center_pos(self, value: Point):
        self.view.centerOn(value.x.base_value, value.y.base_value)

    @property
    def viewport_scale(self) -> float:
        """The interactive viewport's scale (zoom).

        Values should be greater than 0, with 1 as the base zoom and
        larger numbers zooming in.
        """
        # Deriving the scale from the transform matrix is a headache, so compute it by
        # mapping a vector of known length.
        p1 = self.view.mapToScene(QPoint(0, 0))
        p2 = self.view.mapToScene(QPoint(1, 0))
        return 1 / math_helpers.dist((p1.x(), p1.y()), (p2.x(), p2.y()))

    @viewport_scale.setter
    def viewport_scale(self, value: float):
        transform = self.view.viewportTransform()
        relative_scale_factor = value / self.viewport_scale
        self.view.setTransform(
            transform.scale(relative_scale_factor, relative_scale_factor)
        )

    @property
    def viewport_rotation(self) -> float:
        """Set the interactive viewport's rotation angle in degrees.

        The viewport is rotated about its center.
        """
        # Track the rotation explicitly to prevent headaches and ambiguities trying to
        # derive rotation from the viewport transform matrix.
        return self._viewport_rotation

    @viewport_rotation.setter
    def viewport_rotation(self, value: float):
        transform = self.view.viewportTransform()
        if self._viewport_rotation:
            transform = transform.rotate(-self._viewport_rotation)
        self.view.setTransform(transform.rotate(value))
        self._viewport_rotation = value

    def _remove_all_loaded_fonts(self):
        """Remove all fonts registered with ``register_font()``.

        This is primarily useful for testing purposes.
        """
        success = self.font_database.removeAllApplicationFonts()
        if not success:
            raise RuntimeError("Failed to remove application fonts.")

    def clear_scene(self):
        """Clear the QT Scene. This should be called before each render."""
        self.scene.clear()

    def _optimize_for_interactive_view(self):
        QPixmapCache.setCacheLimit(_QT_PIXMAP_CACHE_LIMIT_KB)
        self.view.setViewportUpdateMode(3)  # NoViewportUpdate
        self.scene.setItemIndexMethod(-1)  # NoIndex

    @staticmethod
    def _dpi_to_dpm(dpi: int) -> int:
        """Convert a Dots Per Inch value to Dots Per Meter"""
        return int(dpi / _INCHES_PER_METER)

    @staticmethod
    def _autocrop(q_image: QImage, q_color: QColor) -> QImage:
        """Automatically crop a qt image around the pixels not of a given color.

        Returns a newly cropped image; the original is left unmodified.
        """
        mask = q_image.createMaskFromColor(q_color.rgb())
        crop_rect = QRegion(QBitmap.fromImage(mask)).boundingRect()
        return q_image.copy(crop_rect)
