import os
from brown.core.font import Font


######## Constants that really shouldn't be changed ########

BROWN_ROOT_DIR = os.path.join('..', os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, 'resources')

######## Defaults ##########################################

# Font
DEFAULT_FONT = Font('Cormorant Garamond', 12, 1, False)

# Music Glyph Font
DEFAULT_MUSIC_FONT = 'Gootville'
DEFAULT_MUSIC_FONT_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'gonville-11.otf')

# Print PPI
PRINT_PPI = 300
