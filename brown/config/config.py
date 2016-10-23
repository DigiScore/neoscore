import os


######## Constants that really shouldn't be changed ########

BROWN_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, 'resources')

######## Defaults ##########################################

# Text Font
DEFAULT_TEXT_FONT_NAME = 'Cormorant Garamond'

# Music Glyph Font
DEFAULT_MUSIC_FONT_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'Bravura.otf')
DEFAULT_MUSIC_FONT_NAME = 'Bravura'


# Print PPI
PRINT_PPI = 300

# Staff Height
DEFAULT_STAFF_UNIT = 1  # in millimeters
