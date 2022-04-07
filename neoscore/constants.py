"""package-wide constants"""

import os

from neoscore.core.units import Inch, Mm


def _resolve_bool_env_variable(var):
    value = os.environ.get(var)
    return not (value is None or value == "0" or value.lower() == "false")


# Directories
BROWN_ROOT_DIR = os.path.join(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, "resources")

# Visual gap between pages on the canvas
# (This has no effect on exported documents)
PAGE_DISPLAY_GAP = Mm(50)

# Text Font
DEFAULT_TEXT_FONT_NAME = "Lora"
DEFAULT_TEXT_FONT_SIZE = Mm(2)
DEFAULT_TEXT_FONT_REGULAR_PATH = os.path.join(
    RESOURCES_DIR, "fonts", "lora", "Lora-Regular.ttf"
)
DEFAULT_TEXT_FONT_BOLD_PATH = os.path.join(
    RESOURCES_DIR, "fonts", "lora", "Lora-Bold.ttf"
)
DEFAULT_TEXT_FONT_ITALIC_PATH = os.path.join(
    RESOURCES_DIR, "fonts", "lora", "Lora-Italic.ttf"
)
DEFAULT_TEXT_FONT_BOLD_ITALIC_PATH = os.path.join(
    RESOURCES_DIR, "fonts", "lora", "Lora-BoldItalic.ttf"
)

# Music Glyph Font
DEFAULT_MUSIC_FONT_PATH = os.path.join(RESOURCES_DIR, "fonts", "bravura", "Bravura.otf")
DEFAULT_MUSIC_FONT_METADATA_PATH = os.path.join(
    RESOURCES_DIR, "fonts", "bravura", "bravura_metadata.json"
)
DEFAULT_MUSIC_FONT_NAME = "Bravura"

# Print PPI
PRINT_DPI = Inch.CONVERSION_RATE

# Staff line spacing
DEFAULT_STAFF_UNIT = Mm(1)

# Tab staff line spacing
DEFAULT_TAB_STAFF_SPACING = Mm(1.5)

# Debug Mode
DEBUG = _resolve_bool_env_variable("NEOSCORE_DEBUG")

# QT Runtime
QT_PIXMAP_CACHE_LIMIT_KB = 200_000

# Target time in seconds between frames in animated views
FRAME_REFRESH_TIME_S = 1 / 60

# Target time in seconds between frames in default, non-animated views
DEFAULT_REPL_FRAME_REFRESH_TIME_S = 0.2

HEADLESS_FOR_TEST = _resolve_bool_env_variable("NEOSCORE_HEADLESS")
