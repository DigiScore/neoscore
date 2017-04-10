from brown.utils.units import Mm, Inch


paper_templates = {
    'A4': [Mm(val) for val in [210, 297, 20, 20, 20, 20]],
    'Letter': [Inch(val) for val in [8.5, 11, 1, 1, 1, 1, 0.3]]
}
"""A dictionary of paper templates.

Dict keys are strings and values are `list`s of args to `Paper.__init__()`

Template names are case-insensitive.

Currently supported templates are:
    * `'A4'`
    * `'Letter'`

"""

# TODO: support more templates
