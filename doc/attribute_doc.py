import re


class AttributeDoc:
    """A Python attribute or property as far as docs are concerned."""

    def __init__(self, name, parent, docstring, is_property, is_read_only,
                 default_value=None):
        self.name = name
        self.parent = parent
        self.docstring = docstring
        self.parse_attribute
        self.is_property = is_property
        self.default_value = default_value
        self.type_string = ''
        self.summary = ''
        self.details = ''
        self.parse_attribute()

    def parse_attribute(self):
        first_line, self.details = self.docstring.split('\n\n', 1)
        self.type_string, self.summary = first_line.split(':', 1)
