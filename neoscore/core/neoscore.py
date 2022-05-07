from __future__ import annotations

import json
import os
import pathlib
import tempfile
import threading
from time import time
from typing import TYPE_CHECKING, Callable, Optional, TypeAlias
from warnings import warn

import img2pdf  # type: ignore

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.color import Color, ColorDef
from neoscore.core.exceptions import InvalidImageFormatError
from neoscore.core.paper import A4, Paper
from neoscore.core.pen import Pen
from neoscore.core.rect import RectDef
from neoscore.core.units import Unit
from neoscore.interface.app_interface import AppInterface

if TYPE_CHECKING:
    from neoscore.core.document import Document
    from neoscore.core.font import Font


"""The global state of the application."""

_app_interface: AppInterface

default_font: Font
"""Font: The default font to be used in ``Text`` objects."""

document: Document

registered_music_fonts: dict[str, dict] = {}
"""A map from registered music font names to SMuFL metadata"""

registered_font_family_names: set[str] = set()
"""A set of family names of all registered fonts, including music fonts"""

background_brush = Brush("#ffffff")
"""The scene's background color.

Defaults to white. Set this using ``set_background_brush``.
"""

_supported_image_extensions = {
    ".bmp",
    ".jpg",
    ".jpeg",
    ".png",
    ".pbm",
    ".pgm",
    ".ppm",
    ".xbm",
    ".xpm",
}

# Directories
_FONTS_DIR = pathlib.Path(__file__).parent / ".." / "resources" / "fonts"

# Text Font
_LORA_DIR = _FONTS_DIR / "lora"
_DEFAULT_LORA_FONT_FAMILY_NAME = "Lora"
_DEFAULT_LORA_FONT_SIZE = Unit(12)
_LORA_REGULAR_PATH = _LORA_DIR / "Lora-VariableFont_wght.ttf"
_LORA_ITALIC_PATH = _LORA_DIR / "Lora-Italic-VariableFont_wght.ttf"

# Music Text Font
_BRAVURA_DIR = _FONTS_DIR / "bravura"
_BRAVURA_PATH = _BRAVURA_DIR / "Bravura.otf"
_BRAVURA_METADATA_PATH = _BRAVURA_DIR / "bravura_metadata.json"


def setup(paper: Paper = A4):
    """Initialize the application and set up the global state.

    This initializes the global ``Document`` and a back-end
    AppInterface instance.

    This should be called once at the beginning of every script using ``neoscore``;
    calling this multiple times in one script will cause unexpected behavior.

    Args:
        paper (Paper): The paper to use in the document.

    Returns: None
    """
    global _app_interface
    global default_font
    global document
    global background_brush
    # Some things are imported here to work around cyclic import problems
    from neoscore.core.document import Document
    from neoscore.core.font import Font

    document = Document(paper)
    _app_interface = AppInterface(
        document, _repl_refresh_func, background_brush.interface
    )
    _register_default_fonts()
    default_font = Font(
        _DEFAULT_LORA_FONT_FAMILY_NAME, _DEFAULT_LORA_FONT_SIZE, 1, False
    )


def set_default_color(color: ColorDef):
    """Set the default color used in unspecified pens and brushes.

    This only affects objects created after this is called."""
    # Objects using unspecified pens and brushes make copies of these
    # global default objects.
    c = Color.from_def(color)
    Pen.default_color = c
    Brush.default_color = c


def set_background_brush(brush: BrushDef):
    global background_brush
    global _app_interface
    background_brush = Brush.from_def(brush)
    _app_interface.background_brush = background_brush.interface


def register_font(font_file_path: str) -> list[str]:
    """Register a font file with the application.

    If successful, this makes the font available for use in ``Font`` objects,
    to be referenced by the family name embedded in the font file.

    Args:
        font_file_path: A path to a font file. Currently only
            TrueType and OpenType fonts are supported.

    Returns: A list of family names registered. Typically this will have length 1.

    Raises: FontRegistrationError: If the font could not be loaded.
        Typically, this is because the given path does not lead to
        a valid font file.
    """
    global registered_font_family_names
    global _app_interface
    family_names = _app_interface.register_font(font_file_path)
    for name in family_names:
        registered_font_family_names.add(name)
    return family_names


def register_music_font(font_file_path: str, metadata_path: str):
    """Register a music font with the application.

    Args:
        font_file_path (str): A path to a font file.
        metadata_path (str): A path to a SMuFL metadata JSON file
            for this font. The standard SMuFL format for this file name
            will be {lowercase_font_name}_metadata.json.

    Returns: A list of family names registered. Typically this will have length 1.

    Raises: FontRegistrationError: If the font could not be loaded.
        Typically, this is because the given path does not lead to
        a valid font file.
    """
    global registered_music_fonts
    family_names = register_font(font_file_path)
    try:
        with open(metadata_path, "r") as metadata_file:
            metadata = json.load(metadata_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Music font metadata file {} could not be found".format(metadata_path)
        )
    except json.JSONDecodeError as e:
        e.msg = "Invalid JSON metadata in music font " "metadata file {}".format(
            metadata_path
        )
        raise e
    name = family_names[0]
    if len(family_names) > 1:
        print(
            f"Warning: music font at {font_file_path} contained more than 1 font "
            + f"family. SMuFL metadata will only be stored for {name}."
        )
    registered_music_fonts[name] = metadata


RefreshFunc: TypeAlias = Callable[[float], None]
"""A user-providable function for updating the scene every frame(ish).

The function should accept one argument - the current time in seconds.
"""


def show(refresh_func: Optional[RefreshFunc] = None, display_page_geometry=True):
    """Show a preview of the score in a GUI window.

    An update function can be provided (or otherwise set with
    ``set_refresh_func``) which is run on a timer approximating the
    frame rate.

    The current implementation is pretty limited in features,
    but this could/should be extended in the future once
    the API/interface/Qt bindings are more stable.

    """
    global document
    global _app_interface
    _app_interface._clear_scene()
    document.render()
    if display_page_geometry:
        _render_geometry_preview()
    if refresh_func:
        set_refresh_func(refresh_func)
    _app_interface.show()


def _clear_interfaces():
    global document
    global _app_interface
    _app_interface._clear_scene()
    for page in document.pages:
        for obj in page.descendants:
            interfaces = getattr(obj, "interfaces", None)
            if interfaces:
                interfaces.clear()


def _render_geometry_preview():
    global document
    global background_brush
    for page in document.pages:
        page.render_geometry_preview(background_brush)


def render_pdf(pdf_path: str | pathlib.Path, dpi: int = 300):
    """Render the score as a pdf.

    Args:
        pdf_path (str): The output pdf path
        dpi: Resolution to render with
    """
    global document
    global _app_interface
    _clear_interfaces()
    document.render()
    # Render all pages to temp files
    page_imgs = []
    render_threads = []
    for page in document.pages:
        img_path = tempfile.NamedTemporaryFile(suffix=".png")
        page_imgs.append(img_path)
        render_threads.append(
            render_image(
                page.document_space_bounding_rect,
                img_path.name,
                dpi,
                preserve_alpha=False,
                auto_start_thread=False,
            )
        )
    for thread in render_threads:
        thread.join()
    # Assemble into PDF and write it to file path
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(page_imgs))


def render_image(
    rect: Optional[RectDef],
    image_path: str | pathlib.Path,
    dpi: int = 300,
    quality: int = -1,
    autocrop: bool = False,
    preserve_alpha: bool = True,
    auto_start_thread: bool = True,
) -> threading.Thread:
    """Render a section of the document to an image.

    The following file extensions are supported:
        * ``.bmp``
        * ``.jpg``
        * ``.png``
        * ``.pbm``
        * ``.pgm``
        * ``.ppm``
        * ``.xbm``
        * ``.xpm``

    This renders on the main thread but autocrops and saves the image
    on a spawned thread which is returned to allow efficient rendering
    of many images in parallel. ``render_image`` will block if too many
    render threads are already running.

    Args:
        rect: The part of the document to render, in document coordinates.
            If ``None``, the entire scene will be rendered.
        image_path: The path to the output image.
            This must be a valid path relative to the current working directory.
        dpi: The pixels per inch of the rendered image.
        quality: The quality of the output image for compressed
            image formats. Must be either ``-1`` (default compression) or
            between ``0`` (most compressed) and ``100`` (least compressed).
        autocrop: Whether or not to crop the output image to tightly
            fit the contents of the frame.
        preserve_alpha: Whether to preserve the alpha channel. If false,
            ``neoscore.background_brush`` will be used to flatten any transparency.

    Raises:
        InvalidImageFormatError: If the given ``image_path`` does not have a
            supported image format file extension.
        ImageExportError: If low level Qt image export fails for
            unknown reasons.

    """

    global document
    global _app_interface

    _clear_interfaces()

    if not ((0 <= quality <= 100) or quality == -1):
        warn("render_image quality {} invalid; using default.".format(quality))
        quality = -1

    if not os.path.splitext(image_path)[1] in _supported_image_extensions:
        raise InvalidImageFormatError(
            "image_path {} is not in a supported format.".format(image_path)
        )

    bg_color = background_brush.color
    document.render()

    return _app_interface.render_image(
        rect,
        image_path,
        dpi,
        quality,
        bg_color,
        autocrop,
        preserve_alpha,
    )


def _repl_refresh_func(_: float) -> float:
    """Default refresh func to be used in REPL mode.

    Refreshes at a rate of 5 FPS.
    """
    _clear_interfaces()
    document.render()
    return 0.2


def set_refresh_func(refresh_func: RefreshFunc, target_fps: int = 60):
    global _app_interface
    global document

    frame_wait = 1 / target_fps

    # Wrap the user-provided refresh function with code that clears
    # the scene and re-renders it, then returns the requested delay
    # before the next frame, calculated to automatically compensate
    # for refresh time.
    def wrapped_refresh_func(frame_time: float) -> float:
        _clear_interfaces()
        refresh_func(frame_time)
        document.render()
        elapsed_time = time() - frame_time
        return max(frame_wait - elapsed_time, 0)

    _app_interface.set_refresh_func(wrapped_refresh_func)


def _register_default_fonts():
    register_music_font(
        _BRAVURA_PATH,
        _BRAVURA_METADATA_PATH,
    )
    register_font(_LORA_REGULAR_PATH)
    register_font(_LORA_ITALIC_PATH)


def shutdown():
    _app_interface.destroy()
