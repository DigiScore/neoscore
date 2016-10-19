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
