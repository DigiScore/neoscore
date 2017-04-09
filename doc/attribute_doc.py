from doc.utils import (parse_general_text,
                       parse_type_and_add_code_tag)


class AttributeDoc:
    """A Python attribute or property as far as docs are concerned."""

    def __init__(self, name, parent, docstring, is_property, is_read_only,
                 default_value, global_index):
        self.name = name
        self.parent = parent
        self.docstring = docstring
        self.is_property = is_property
        self.is_read_only = is_read_only
        self.default_value = default_value
        self.global_index = global_index
        self.global_index.add(self)
        self.type_string = ''
        self.summary = ''
        self.details = ''

    @property
    def html_id(self):
        if type(self.parent).__name__ == 'ClassDoc':
            return self.parent.name + '.' + self.name
        else:
            return self.name

    @property
    def url(self):
        if type(self.parent).__name__ == 'ClassDoc':
            return self.parent.url + '.' + self.name
        else:
            return self.parent.url + '#' + self.name

    def resolve_names_and_parse_html(self):
        if '\n\n' in self.docstring:
            first_line, self.details = self.docstring.split('\n\n', 1)
        else:
            first_line = self.docstring
            self.details = ''
        if ':' in first_line:
            self.type_string, self.summary = first_line.split(':', 1)
            self.type_string = parse_type_and_add_code_tag(
                self.type_string, self.parent)
        else:
            self.type_string = ''
            self.summary = first_line
        self.summary = self.summary.replace('\n', '')
        self.summary = parse_general_text(self.summary, self.parent,
                                          split_paragraphs=False)
