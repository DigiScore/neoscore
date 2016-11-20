"""
Various units as ratios to pixels
"""

from brown.config import config


# Include a reference to backend? In case graphics engine
# expects something different


pixel = 1
inch = config.PRINT_PPI * pixel
mm = inch / 25.4
cm = mm * 10
# A staff unit is defined as the distance between two lines
# in a staff. For now, this depends on the assumption that
# all staves will have exactly 5 lines, and that all staves
# are the same size, as defined in config.DEFAULT_STAFF_HEIGHT
staff_unit = config.DEFAULT_STAFF_UNIT
