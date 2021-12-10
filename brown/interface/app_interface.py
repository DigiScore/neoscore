import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtPrintSupport import QPrinter

from brown import constants
from brown.earle.ui.main_window import MainWindow
from brown.interface import images
from brown.interface.interface import Interface
from brown.interface.qt.converters import rect_to_qt_rect_f, color_to_q_color
from brown.utils.exceptions import (FontRegistrationError,
                                    ImageExportError)
from brown.utils.units import Unit, Meter


class AppInterface(Interface):
    """The primary interface to the application state.

    This holds much of the global state for interacting with the API,
    and must be created (and `create_document()` must be called) before
    working with the API.
    """

    _QT_FONT_ERROR_CODE = -1

    def __init__(self, document):
        """
        Args:
            document (Document):
        """
        super().__init__(None)  # no brown object exists for this
                                # TODO: make one
        self.document = document
        self.app = QtWidgets.QApplication([])
        self.main_window = MainWindow()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = self.main_window.graphicsView
        self.view.setScene(self.scene)
        self.registered_music_fonts = {}
        self.font_database = QtGui.QFontDatabase()

    ######## PUBLIC METHODS ########

    def show(self):
        """Open a window showing a preview of the document."""
        self.main_window.show()
        self.app.exec_()
    
    def _clear_scene(self):
        """Clear the QT Scene. This should be called before each render."""
        self.scene.clear()

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
        printer.setPageLayout(self.document.paper._to_interface())
        painter = QtGui.QPainter()
        painter.begin(printer)
        # Scaling ratio for Qt point 72dpi -> constants.PRINT_DPI
        ratio = (constants.PRINT_DPI / 72)
        target_rect_unscaled = printer.paperRect(QPrinter.Point)
        target_rect_scaled = QtCore.QRectF(
            target_rect_unscaled.x() * ratio,
            target_rect_unscaled.y() * ratio,
            target_rect_unscaled.width() * ratio,
            target_rect_unscaled.height() * ratio,
        )
        for page_number in pages:
            source_rect = rect_to_qt_rect_f(
                self.document.paper_bounding_rect(page_number))
            self.scene.render(painter,
                              target=target_rect_scaled, source=source_rect)
            printer.newPage()
        painter.end()

    def render_image(self, rect, image_path, dpm, quality, bg_color, autocrop):
        """Render a section of self.scene to an image.

        It is assumed that all input arguments are valid.

        Args:
            rect (Rect): The part of the document to render,
                in document coordinates.
            image_path (str): The path to the output image.
                This must be a valid path relative to the current
                working directory.
            dpm (int): The pixels per meter of the rendered image.
            quality (int): The quality of the output image for compressed
                image formats. Must be either `-1` (default compression) or
                between `0` (most compressed) and `100` (least compressed).
            bg_color (Color): The background color for the image.
            autocrop (bool): Whether or not to crop the output image to tightly
                fit the contents of the frame. If true, the image will be
                cropped such that all 4 edges have at least one pixel not of
                `bg_color`.

        Returns: None

        Raises:
            ImageExportError: If Qt image export fails for unknown reasons.
        """
        scale_factor = dpm / Unit(Meter(1)).value
        pix_width = Unit(rect.width).value * scale_factor
        pix_height = Unit(rect.height).value * scale_factor

        q_image = QtGui.QImage(pix_width, pix_height,
                               QtGui.QImage.Format_ARGB32)
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
                'Unknown error occurred when exporting image to ' + image_path)

    def destroy(self):
        """Destroy the window and all global interface-level data."""
        print('Tearing down Qt Application instance')
        self.app.exit()
        self.app = None
        self.scene = None

    def register_font(self, font_file_path):
        """Register a font file with the graphics engine.

        Args:
            font_file_path (str): A path to a font file. The path should
                be relative to the main `brown` package. Currently only
                TrueType and OpenType fonts are supported.

        Returns: None

        Raises: FontRegistrationError: if the registration fails.
        """
        font_id = self.font_database.addApplicationFont(font_file_path)
        if font_id == AppInterface._QT_FONT_ERROR_CODE:
            raise FontRegistrationError(font_file_path)

    def _remove_all_loaded_fonts(self):
        """Remove all fonts registered with `register_font()`.

        This is primarily useful for testing purposes.
        """
        success = self.font_database.removeAllApplicationFonts()
        if not success:
            raise RuntimeError('Failed to remove application fonts.')
