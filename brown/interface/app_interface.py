from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import QPrinter

from brown import constants
from brown.interface import images
from brown.interface.qt.converters import color_to_q_color, rect_to_qt_rect_f
from brown.interface.qt.main_window import MainWindow
from brown.utils.color import Color
from brown.utils.exceptions import FontRegistrationError, ImageExportError
from brown.utils.rect import Rect
from brown.utils.units import Meter

if TYPE_CHECKING:
    from brown.core.document import Document


class AppInterface:
    """The primary interface to the application state.

    This holds much of the global state for interacting with the API,
    and must be created (and `create_document()` must be called) before
    working with the API.
    """

    _QT_FONT_ERROR_CODE = -1

    def __init__(self, document: Document):
        self.document = document
        self.app = QtWidgets.QApplication([])
        self.main_window = MainWindow()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = self.main_window.graphicsView
        self.view.setScene(self.scene)
        self.registered_music_fonts = {}
        self.font_database = QtGui.QFontDatabase()

    ######## PUBLIC METHODS ########

    def set_refresh_func(self, refresh_func: Callable[[float], None]):
        self.main_window.refresh_func = refresh_func

    def show(self):
        """Open a window showing a preview of the document."""
        self._optimize_for_interactive_view()
        self.main_window.show()
        self.app.exec_()

    def render_pdf(self, pages, path):
        """Render the document to a pdf file.

        Args:
            pages (iter[int]): The page numbers to render
            path (str): An output file path.

        Warning: If the file at `path` already exists, it will be overwritten.
        """
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(os.path.realpath(path))
        printer.setResolution(constants.PRINT_DPI)
        printer.setPageLayout(self.document.paper.interface.qt_object)
        painter = QtGui.QPainter()
        painter.begin(printer)
        # Scaling ratio for Qt point 72dpi -> constants.PRINT_DPI
        ratio = constants.PRINT_DPI / 72
        target_rect_unscaled = printer.paperRect(QPrinter.Point)
        target_rect_scaled = QtCore.QRectF(
            target_rect_unscaled.x() * ratio,
            target_rect_unscaled.y() * ratio,
            target_rect_unscaled.width() * ratio,
            target_rect_unscaled.height() * ratio,
        )
        for page_number in pages:
            source_rect = rect_to_qt_rect_f(
                self.document.paper_bounding_rect(page_number)
            )
            self.scene.render(painter, target=target_rect_scaled, source=source_rect)
            printer.newPage()
        painter.end()

    def render_image(
        self,
        rect: Rect,
        image_path: str,
        dpm: int,
        quality: int,
        bg_color: Color,
        autocrop: bool,
    ):
        """Render a section of self.scene to an image.

        It is assumed that all input arguments are valid.

        Args:
            rect: The part of the document to render,
                in document coordinates.
            image_path: The path to the output image.
                This must be a valid path relative to the current
                working directory.
            dpm: The pixels per meter of the rendered image.
            quality: The quality of the output image for compressed
                image formats. Must be either `-1` (default compression) or
                between `0` (most compressed) and `100` (least compressed).
            bg_color: The background color for the image.
            autocrop: Whether or not to crop the output image to tightly
                fit the contents of the frame. If true, the image will be
                cropped such that all 4 edges have at least one pixel not of
                `bg_color`.

        Raises:
            ImageExportError: If Qt image export fails for unknown reasons.
        """
        scale = dpm / Meter(1).base_value
        pix_width = int(rect.width.base_value * scale)
        pix_height = int(rect.height.base_value * scale)

        q_image = QtGui.QImage(pix_width, pix_height, QtGui.QImage.Format_ARGB32)
        q_image.setDotsPerMeterX(dpm)
        q_image.setDotsPerMeterY(dpm)
        q_color = color_to_q_color(bg_color)
        q_image.fill(q_color)

        painter = QtGui.QPainter()
        painter.begin(q_image)

        target_rect = QtCore.QRectF(q_image.rect())
        source_rect = rect_to_qt_rect_f(rect)

        self.scene.render(painter, target=target_rect, source=source_rect)
        painter.end()

        if autocrop:
            q_image = images.autocrop(q_image, q_color)

        success = q_image.save(image_path, quality=quality)

        if not success:
            raise ImageExportError(
                "Unknown error occurred when exporting image to " + image_path
            )

    def destroy(self):
        """Destroy the window and all global interface-level data."""
        print("Tearing down Qt Application instance")
        self.app.exit()
        self.app = None
        self.scene = None

    def register_font(self, font_file_path: str) -> list[str]:
        """Register a font file with the graphics engine.

        Args:
            font_file_path: A path to a font file. The path should
                be relative to the main `brown` package. Currently only
                TrueType and OpenType fonts are supported.

        Returns: A list of font families found in the font.

        Raises: FontRegistrationError: if the registration fails.
        """
        font_id = self.font_database.addApplicationFont(font_file_path)
        if font_id == AppInterface._QT_FONT_ERROR_CODE:
            raise FontRegistrationError(font_file_path)
        family_names = self.font_database.applicationFontFamilies(font_id)
        if not len(family_names):
            # I think this should be impossible, but log a warning just in case
            print(f"Warning: font at {font_file_path} provided no family names")
        return self.font_database.applicationFontFamilies(font_id)

    ######## PRIVATE METHODS ########

    def _remove_all_loaded_fonts(self):
        """Remove all fonts registered with `register_font()`.

        This is primarily useful for testing purposes.
        """
        success = self.font_database.removeAllApplicationFonts()
        if not success:
            raise RuntimeError("Failed to remove application fonts.")

    def _clear_scene(self):
        """Clear the QT Scene. This should be called before each render."""
        self.scene.clear()

    def _optimize_for_interactive_view(self):
        QtGui.QPixmapCache.setCacheLimit(constants.QT_PIXMAP_CACHE_LIMIT_KB)
