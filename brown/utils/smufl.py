import json
import os

from brown.config import config

# Load metadata into dictionaries

smufl_dir = os.path.join(config.RESOURCES_DIR, 'smufl')

with open(os.path.join(smufl_dir, 'classes.json'), 'r') as classes_file:
    classes = json.load(classes_file)

with open(os.path.join(smufl_dir, 'glyphnames.json'), 'r') as glyphnames_file:
    glyph_names = json.load(glyphnames_file)

with open(os.path.join(smufl_dir, 'ranges.json'), 'r') as ranges_file:
    ranges = json.load(ranges_file)
