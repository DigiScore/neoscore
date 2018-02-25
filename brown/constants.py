"""package-wide constants"""

import os

from brown.utils.units import Mm, Inch, GraphicUnit
from brown.core.pen_pattern import PenPattern
from brown.core.brush_pattern import BrushPattern
from brown.utils.color import Color


# Directories
BROWN_ROOT_DIR = os.path.join(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, 'resources')
UI_DIR = os.path.join(BROWN_ROOT_DIR, 'earle', 'ui')

# Default pen properties
DEFAULT_PEN_COLOR = Color(0, 0, 0)
DEFAULT_PEN_THICKNESS = GraphicUnit(0)  # GraphicUnits
DEFAULT_PEN_PATTERN = PenPattern.SOLID

# Default brush properties
DEFAULT_BRUSH_COLOR = Color(0, 0, 0, 255)
DEFAULT_PATH_BRUSH_COLOR = Color(0, 0, 0, 0)
DEFAULT_BRUSH_PATTERN = BrushPattern.SOLID

# Paper type
DEFAULT_PAPER_TYPE = 'Letter'

# Visual gap between pages on the canvas
# (This has no effect on exported documents)
PAGE_DISPLAY_GAP = Mm(150)

# Text Font
DEFAULT_TEXT_FONT_NAME = 'Lora'
DEFAULT_TEXT_FONT_SIZE = Mm(2)
DEFAULT_TEXT_FONT_REGULAR_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'lora', 'Lora-Regular.ttf')
DEFAULT_TEXT_FONT_BOLD_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'lora', 'Lora-Bold.ttf')
DEFAULT_TEXT_FONT_ITALIC_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'lora', 'Lora-Italic.ttf')
DEFAULT_TEXT_FONT_BOLD_ITALIC_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'lora', 'Lora-BoldItalic.ttf')

# Music Glyph Font
DEFAULT_MUSIC_FONT_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'bravura', 'Bravura.otf')
DEFAULT_MUSIC_FONT_METADATA_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'bravura', 'bravura_metadata.json')
DEFAULT_MUSIC_FONT_NAME = 'Bravura'

# Print PPI
PRINT_DPI = Inch.CONVERSION_RATE

# Staff Height
DEFAULT_STAFF_UNIT = Mm(1)
