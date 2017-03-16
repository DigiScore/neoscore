import json

from brown import config
from brown.core.document import Document
from brown.core.font import Font
from brown.interface.app_interface import AppInterface, FontRegistrationError

"""The global state of the application."""

# Fetch and initialize app interface
_app_interface_class = AppInterface
_app_interface = None
text_font = None
document = None
registered_music_fonts = {}
registered_text_fonts = {}

# Color of background between and around pages. (Not yet implemented)
_display_background_color = '#dddddd'
# Background color of pages themselves. (Not yet implemented)
_display_paper_color = '#ffffff'


def setup(initial_paper=None):
    """Initialize the application and set up the global state.

    This initializes the global `Document` and a back-end
    AppInterface instance.

    This should be called once at the beginning of every script using `brown`;
    calling this multiple times in one script will cause unexpected behavior.

    Args:
        paper (Paper): The paper to use in the document. If None,
                this defaults to config.DEFAULT_PAPER_TYPE

    Returns: None
    """
    global _app_interface
    global text_font
    global paper
    global document
    global registered_text_fonts
    document = Document(initial_paper)
    _app_interface = _app_interface_class(document)
    _, music_font_json = register_music_font(
        config.DEFAULT_MUSIC_FONT_PATH,
        config.DEFAULT_MUSIC_FONT_METADATA_PATH)
    # TODO: There is probably a better way/name/explanation
    #       for how the global default font is handled here.
    text_font = Font(config.DEFAULT_TEXT_FONT_NAME,
                     config.DEFAULT_TEXT_FONT_SIZE,
                     1,
                     False)


def register_music_font(font_file_path, metadata_path):
    """Register a music font with the graphics engine and load its metadata.

    Args:
        font_file_paths (str): A path to a font file.
            Path may be either absolute or relative to the package-level
            `brown` directory. (One folder below the top)
        metadata_path (str): A path to a SMuFL metadata JSON file
            for this font.

    Returns:
        int: The id for the newly registered font
        dict: The metadata for the new font
    """
    global _app_interface
    global registered_music_fonts
    # TODO: The whole app-level implementation of music fonts is pretty
    #       awkward and hacky right now. After working out main smufl
    #       functionality, it will probably be good to rework the way
    #       is handled at the application level
    try:
        font_id = _app_interface.register_font(font_file_path)
    except FontRegistrationError:
        raise FontRegistrationError(
            'Font loaded from {} failed'.format(font_file_path))
    try:
        with open(metadata_path, 'r') as metadata_file:
            metadata = json.load(metadata_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            'Music font metadata file {} could not be found'.format(metadata_path))
    except json.JSONDecodeError:
        raise json.JSONDecodeError(
            'Invalid JSON metadata in music font '
            'metadata file {}'.format(metadata_path))
    registered_music_fonts[config.DEFAULT_MUSIC_FONT_NAME] = metadata
    return font_id, metadata


def show():
    """Show a preview of the score in a GUI window.

    The current implementation is pretty limited in features,
    but this could/should be extended in the future once
    the API/interface/Qt bindings are more stable.

    Returns: None
    """
    global document
    global _app_interface
    document.render()
    _app_interface.show()


def render_pdf(path):
    """Render the score as a pdf.

    Args:
        path (str): The output score path.
            If a relative path is provided, it will be
            relative to the current working directory.
    """
    global document
    global _app_interface
    document.render()
    _app_interface.render_pdf(document.occupied_pages, path)
