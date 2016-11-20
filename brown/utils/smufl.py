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


def look_up_glyph_name(name):
    """Find the {"codepoint", "description"} dict for a given glyph name.

    Args:
        name (str): The name of the glyph

    Returns:
        dict {"codepoint": str, "description": str}: Information on the glyph

    Raises:
        KeyError: If no glyph with `name` can be found
    """
    try:
        return glyph_names[name]
    except KeyError:
        # TODO: Implement a fuzzy look-up for a (Did you mean ... ? response)
        raise KeyError('Could not find glyph name "{}".')


def char_from_glyph_name(name):
    """Find the unicode character for a given glyph name

    Args:
        name (str): The name of the glyph

    Returns:
        str: The unicode character corresponding to the glyph name

    Raises:
        KeyError: If no glyph with `name` can be found
    """
    try:
        return look_up_glyph_name(name)['codepoint']
    except KeyError:
        raise KeyError


def description_from_glyph_name(name):
    """Find the description for a given glyph name

    Args:
        name (str): The name of the glyph

    Returns:
        str: The glyph's short description

    Raises:
        KeyError: If no glyph with `name` can be found
    """
    try:
        return look_up_glyph_name(name)['description']
    except KeyError:
        raise KeyError
