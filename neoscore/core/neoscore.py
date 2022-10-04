from __future__ import annotations

import json
import os
import pathlib
from time import time
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Set, Tuple
from warnings import warn

import img2pdf  # type: ignore
from typing_extensions import TypeAlias

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.color import Color, ColorDef
from neoscore.core.exceptions import InvalidImageFormatError
from neoscore.core.key_event import KeyEvent
from neoscore.core.mouse_event import MouseEvent
from neoscore.core.paper import A4, Paper
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.propagating_thread import PropagatingThread
from neoscore.core.rect import RectDef
from neoscore.core.units import Unit
from neoscore.interface.app_interface import AppInterface

if TYPE_CHECKING:
    from neoscore.core.document import Document
    from neoscore.core.font import Font


"""The global application state module."""

default_font: Font
"""The default font to be used in ``Text`` objects."""

document: Document
"""The root document object."""

registered_music_fonts: Dict[str, dict] = {}
"""A map from registered music font names to SMuFL metadata"""

registered_font_family_names: Set[str] = set()
"""A set of family names of all registered fonts, including music fonts"""

background_brush = Brush("#ffffff")
"""The brush used to draw the scene background.

Defaults to solid white. Set this using :obj:`.set_background_brush`.
"""

app_interface: AppInterface
"""The underlying application interface.

You generally shouldn't directly interact with this.
"""

_display_page_geometry_in_refresh_func: bool = False
"""Whether to render the page geometry in refresh renders.

This global serves as a bit of a hack for passing the "display page geometry?" flag into
refresh functions.
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
        paper: The paper to use in the document.
    """
    global app_interface
    global default_font
    global document
    global background_brush
    # Some things are imported here to work around cyclic import problems
    from neoscore.core.document import Document
    from neoscore.core.font import Font

    document = Document(paper)

    app_interface = AppInterface(
        document, _repl_refresh_func, background_brush.interface, True
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
    Pen._default_color = c
    Brush._default_color = c


def set_background_brush(brush: BrushDef):
    """Set the brush used to paint the scene background."""
    global background_brush
    global app_interface
    background_brush = Brush.from_def(brush)
    app_interface.background_brush = background_brush.interface


def register_font(font_file_path: str | pathlib.Path) -> List[str]:
    """Register a font file with the application.

    If successful, this makes the font available for use in :obj:`.Font` objects,
    to be referenced by the family name embedded in the font file.

    Args:
        font_file_path: A path to a font file. Only TrueType and OpenType
            fonts are supported.

    Returns:
        A list of family names registered. Typically, this will have length 1.

    Raises:
        FontRegistrationError: If the font could not be loaded.
            Typically, this is because the given path does not lead to
            a valid font file.
    """
    global registered_font_family_names
    global app_interface
    family_names = app_interface.register_font(font_file_path)
    for name in family_names:
        registered_font_family_names.add(name)
    return family_names


def register_music_font(
    font_file_path: str | pathlib.Path, metadata_path: str | pathlib.Path
):
    """Register a music font with the application.

    Args:
        font_file_path: A path to a font file.
        metadata_path: A path to a SMuFL metadata JSON file
            for this font. The standard SMuFL format for this file name
            will be ``{lowercase_font_name}_metadata.json``.

    Returns:
        A list of family names registered. Typically, this will have length 1.

    Raises:
        FontRegistrationError: If the font could not be loaded.
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

Refresh functions can modify the scene, create new objects, and :obj:`remove
<.PositionedObject.remove>` them, though not all objects respond well to mutability.
"""


def show(
    refresh_func: Optional[RefreshFunc] = None,
    display_page_geometry=True,
    auto_viewport_interaction_enabled=True,
    min_window_size: Optional[Tuple[int, int]] = None,
    max_window_size: Optional[Tuple[int, int]] = None,
    fullscreen: bool = False,
):
    """Display the score in an interactive GUI window.

    Args:
        refresh_func: A scene update function to run on a timer approximating the
            frame rate. This can also be set with :obj:`.set_refresh_func`, which
            allows customizing the target frame rate.
        display_page_geometry: Whether to include a preview of page geometry,
            including a page outline and a dotted outline of the page's live
            area inside its margins.
        auto_viewport_interaction_enabled: Whether mouse and scrollbar viewport
            interaction is enabled. If false, scrollbars do not appear, mousewheel
            zooming is disabled, and click-and-drag view movement is disabled.
        min_window_size: An optional ``(width, height)`` minimum window size tuple.
        max_window_size: An optional ``(width, height)`` maximum window size tuple.
        fullscreen: Whether to show the window in fullscreen mode.
            This doesn't mix well with ``max_window_size``.
    """
    global app_interface
    global background_brush
    global document
    global _display_page_geometry_in_refresh_func
    _display_page_geometry_in_refresh_func = display_page_geometry
    app_interface.clear_scene()
    document.render(display_page_geometry, background_brush)
    if refresh_func:
        set_refresh_func(refresh_func)
    app_interface.auto_viewport_interaction_enabled = auto_viewport_interaction_enabled
    app_interface.show(min_window_size, max_window_size, fullscreen)


def _clear_interfaces():
    global document
    global app_interface
    app_interface.clear_scene()
    for page in document.pages:
        for obj in page.descendants:
            interfaces = getattr(obj, "interfaces", None)
            if interfaces:
                interfaces.clear()
            if hasattr(obj, "_interface_for_children"):
                obj._interface_for_children = None


def set_viewport_center_pos(document_pos: PointDef):
    """Center the interactive viewport at a given document-space position.

    If the given position is such that the requested view goes beyond the document's
    bounding rect, the actual position used is adjusted to prevent that. This is caused
    by an internal limitation and may change in the future. To work around this issue,
    you can expand the document bounding rect by creating an arbitrarily large invisible
    path like so::

        Path.rect((Mm(-1000000), Mm(-1000000)), None, Mm(2000000), Mm(2000000),
              Brush.no_brush(), Pen.no_pen())

    This is mostly recommended when not using automatic viewport interaction.
    """
    global app_interface
    app_interface.viewport_center_pos = Point.from_def(document_pos)


def get_viewport_center_pos() -> Point:
    """Return the interactive viewport's center position in document-space.

    This value may differ slightly from values set in ``set_viewport_center_pos``.
    """
    global app_interface
    return app_interface.viewport_center_pos


def set_viewport_scale(scale: float):
    """Set the interactive viewport's scale (zoom).

    Values should be greater than 0, with 1 as the base zoom and
    larger numbers zooming in.
    """
    global app_interface
    app_interface.viewport_scale = scale


def get_viewport_scale() -> float:
    """Return the interactive viewport's scale (zoom).

    This value is always greater than 0, with 1 as the base zoom and
    larger numbers zooming in.

    This value may differ slightly from values set in ``set_viewport_scale``.
    """
    global app_interface
    return app_interface.viewport_scale


def set_viewport_rotation(rotation: float):
    """Set the interactive viewport's rotation angle in degrees.

    The viewport is rotated about its center.
    """
    global app_interface
    app_interface.viewport_rotation = rotation


def get_viewport_rotation() -> float:
    """Return the interactive viewport's rotation angle in degrees."""
    global app_interface
    return app_interface.viewport_rotation


def render_pdf(pdf_path: str | pathlib.Path, dpi: int = 300):
    """Render the score as a pdf.

    Args:
        pdf_path: The output pdf path
        dpi: Resolution to render at
    """
    global app_interface
    global background_brush
    global document
    _clear_interfaces()
    document.render(False, background_brush)
    # Render all pages to temp files
    page_imgs = []
    render_threads = []
    for page in document.pages:
        img_buffer = bytearray()
        page_imgs.append(img_buffer)
        render_threads.append(
            render_image(
                page.document_space_bounding_rect,
                img_buffer,
                dpi,
                preserve_alpha=False,
                wait=False,
            )
        )
    for thread in render_threads:
        thread.join()
    # Assemble into PDF and write it to file path
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([bytes(buf) for buf in page_imgs]))


def render_image(
    rect: Optional[RectDef],
    dest: str | pathlib.Path | bytearray,
    dpi: int = 300,
    quality: int = -1,
    autocrop: bool = False,
    preserve_alpha: bool = True,
    wait: bool = True,
) -> PropagatingThread:
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

    If `wait == False`, this renders on the main thread but autocrops and saves the
    image on a spawned thread which is returned to allow efficient rendering of many
    images in parallel.

    Args:
        rect: The part of the document to render, in document coordinates.
            If ``None``, the entire scene will be rendered.
        dest: An output file path or a bytearray to save to. If a bytearray
            is given, the output format will be PNG.
        dpi: The pixels per inch of the rendered image. quality: The quality of the
        output image for compressed
            image formats. Must be either ``-1`` (default compression) or between ``0``
            (most compressed) and ``100`` (least compressed).
        autocrop: Whether to crop the output image to tightly
            fit the contents of the frame.
        preserve_alpha: Whether to preserve the alpha channel. If false,
            ``neoscore.background_brush`` will be used to flatten any transparency.
        wait: Whether to block until the image is fully exported.

    Raises:
        InvalidImageFormatError: If the given ``image_path`` does not have a
            supported image format file extension.
        ImageExportError: If low level Qt image export fails for
            unknown reasons.
    """

    global app_interface
    global background_brush
    global document

    _clear_interfaces()

    if not ((0 <= quality <= 100) or quality == -1):
        warn("render_image quality {} invalid; using default.".format(quality))
        quality = -1

    if (
        not isinstance(dest, bytearray)
        and not os.path.splitext(dest)[1] in _supported_image_extensions
    ):
        raise InvalidImageFormatError(
            "image_path {} is not in a supported format.".format(dest)
        )

    bg_color = background_brush.color
    document.render(False, background_brush)

    thread = app_interface.render_image(
        rect,
        dest,
        dpi,
        quality,
        bg_color,
        autocrop,
        preserve_alpha,
    )
    if wait:
        thread.join()
    return thread


def _repl_refresh_func(_: float) -> float:
    """Default refresh func to be used in REPL mode.

    Refreshes at a rate of 5 FPS.
    """
    global background_brush
    global document
    global _display_page_geometry_in_refresh_func
    _clear_interfaces()
    document.render(_display_page_geometry_in_refresh_func, background_brush)
    return 0.2


def set_refresh_func(refresh_func: RefreshFunc, target_fps: int = 60):
    """Update the global scene refresh function.

    Args:
        refresh_func: The new refresh function
        target_fps: The requested frame rate to run the function at.
    """
    global app_interface
    global document
    global background_brush
    global _display_page_geometry_in_refresh_func

    frame_wait = 1 / target_fps

    # Wrap the user-provided refresh function with code that clears
    # the scene and re-renders it, then returns the requested delay
    # before the next frame, calculated to automatically compensate
    # for refresh time.
    def wrapped_refresh_func(frame_time: float) -> float:
        _clear_interfaces()
        refresh_func(frame_time)
        document.render(_display_page_geometry_in_refresh_func, background_brush)
        elapsed_time = time() - frame_time
        return max(frame_wait - elapsed_time, 0)

    app_interface.set_refresh_func(wrapped_refresh_func)


def set_mouse_event_handler(handler: Callable[[MouseEvent], None]):
    """Set the global mouse event handler function.

    Mouse events are fired on mouse moves and button presses, releases, and double
    clicks.

    Args:
        handler: A callback function which accepts a mouse event.
            See :obj:`.MouseEvent` for what event data is provided.

    """
    global app_interface
    app_interface.set_mouse_event_handler(handler)


def set_key_event_handler(handler: Callable[[KeyEvent], None]):
    """Set the global key event handler function.

    Key events are fired on key presses, releases, and auto-repeats from being held.

    Args:
        handler: A callback function which accepts a key event.
            See :obj:`.KeyEvent` for what event data is provided.

    """
    global app_interface
    app_interface.set_key_event_handler(handler)


def _register_default_fonts():
    register_music_font(
        _BRAVURA_PATH,
        _BRAVURA_METADATA_PATH,
    )
    register_font(_LORA_REGULAR_PATH)
    register_font(_LORA_ITALIC_PATH)


def shutdown():
    """Tear down the global state, including the document tree.

    After running this, :obj:`.neoscore.setup` can be called again to start a new
    document.
    """
    app_interface.destroy()
