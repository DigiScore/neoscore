"""
A module containing a dict of paper templates for easy Paper initialization

Dict keys are strings and values are tuples of args to `Paper.__init__()`

Template names are case-insensitive.
"""

from brown.utils.units import Mm, Inch


paper_templates = {
    'A4': [Mm(val) for val in [210, 297, 20, 20, 20, 20]],
    'Letter': [Inch(val) for val in [8.5, 11, 1, 1, 1, 1, 0.3]]
}

# TODO: support more templates
