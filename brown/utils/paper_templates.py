"""
A module containing a dict of paper templates for easy Paper initialization

Dict keys are strings and values are tuples of args to `Paper.__init__()`

Template names are case-insensitive.
"""

paper_templates = {
    'A4': (210, 297, 20, 30, 20, 30, 15),
}

# TODO: support more templates
