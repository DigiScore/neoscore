"""SMuFL spec metadata loaded into module constants."""
import json
import pathlib

# Load metadata into dictionaries

_SMUFL_DIR = pathlib.Path(__file__).parent / ".." / "resources" / "smufl"

classes: dict
"""The raw SMuFL ``classes.json`` metadata.

See https://w3c.github.io/smufl/latest/specification/classes.html

:meta hide-value:
"""

glyph_names: dict
"""The raw SMuFL ``glyphnames.json`` metadata.

See https://w3c.github.io/smufl/latest/specification/glyphnames.html

:meta hide-value:
"""

ranges: dict
"""The raw SMuFL ``ranges.json`` metadata.

See https://w3c.github.io/smufl/latest/specification/ranges.html

:meta hide-value:
"""

with open(_SMUFL_DIR / "classes.json", "r") as classes_file:
    classes = json.load(classes_file)

with open(_SMUFL_DIR / "glyphnames.json", "r") as glyphnames_file:
    glyph_names = json.load(glyphnames_file)

with open(_SMUFL_DIR / "ranges.json", "r") as ranges_file:
    ranges = json.load(ranges_file)
