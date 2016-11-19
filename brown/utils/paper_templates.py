"""
A module containing a dict of paper templates for easy Paper initialization

Dict keys are strings and values are tuples of args to `Paper.__init__()`

Template names are case-insensitive.
"""

from brown.utils.mm import Mm


paper_templates = {
    'A4': [Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]],
}

# TODO: support more templates
