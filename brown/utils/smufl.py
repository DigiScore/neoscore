import json
import os

from brown import constants

# Load metadata into dictionaries

smufl_dir = os.path.join(constants.RESOURCES_DIR, 'smufl')

with open(os.path.join(smufl_dir, 'classes.json'), 'r') as classes_file:
    classes = json.load(classes_file)

with open(os.path.join(smufl_dir, 'glyphnames.json'), 'r') as glyphnames_file:
    glyph_names = json.load(glyphnames_file)

with open(os.path.join(smufl_dir, 'ranges.json'), 'r') as ranges_file:
    ranges = json.load(ranges_file)


def get_basic_glyph_info(name):
    """Find the {"codepoint", "description"} dict for a canonical glyph name.

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
        return get_basic_glyph_info(name)['codepoint']
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
        return get_basic_glyph_info(name)['description']
    except KeyError:
        raise KeyError


def get_glyph_range_key(name):
    """Find the range the glyph with `name` belongs to.

    Args:
        name (str): The name of the glyph

    Returns:
        str: The key for `ranges` of the range the glyph belongs in

    Raises:
        KeyError: If no glyph with `name` can be found in `ranges`
    """
    for range_name, value in ranges.items():
        if name in value['glyphs']:
            return range_name
    else:
        raise KeyError('Could not find glyph name "{}".')


def get_glyph_classes(name):
    """Find all of the classes the glyph with `name` belongs in.

    Args:
        name (str): The name of the glyph

    Returns:
        set[str]: The classes the glyph belongs in

    Raises:
        KeyError: If no glyph with `name` can be found in `ranges`

    Warning:
        This is potentially a slow function. If it starts being used a lot,
        probably consider building a more efficient data structure around
        this look-up.
    """
    matches = set()
    for class_name, class_glyphs in classes.items():
        if name in class_glyphs:
            matches.add(class_name)
    return matches
