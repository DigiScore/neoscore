import re

from doc.attribute_doc import AttributeDoc
from doc.method_doc import MethodDoc
from doc.method_type import MethodType
from doc.utils import (previous_line_ending_index_from,
                       first_or_none,
                       whole_line_at,
                       parse_general_text,
                       surround_with_tag,
                       parse_type_and_add_code_tags,
                       parse_type_string)


class ClassDoc:
    """A Python class as far as docs are concerned."""

    docstring_re = re.compile(
        r'(\"\"\"(?P<content>.*?)\"\"\")',
        flags=re.DOTALL)
    method_re = re.compile(r'^ +def (?P<method>[a-z_][A-Za-z_0-9]*)'
                                    '\((?P<args>.*?)\):\n',
                                    flags=re.DOTALL | re.MULTILINE)
    staticmethod_re = re.compile(r'^ +\@staticmethod\n',
                                 flags=re.MULTILINE)
    classmethod_re = re.compile(r'^ +\@classmethod\n',
                                flags=re.MULTILINE)
    property_re = re.compile(r'^ +\@property\n',
                             flags=re.MULTILINE)
    setter_re = re.compile(r'^ +\@(?P<name>\w+)\.setter\n',
                           flags=re.MULTILINE)
    attribute_re = re.compile(r'^    (?P<name>\w+) = (?P<value>.*$)\n',
                              flags=re.MULTILINE)
    warning_re = re.compile(r'^ *Warning:\s*(?P<body>.*?)\n(\n| *?\Z)',
                            flags=re.DOTALL | re.MULTILINE)

    def __init__(self, name, parent, superclass_string, docstring, body,
                 global_index):
        # Parent can be a ModuleDoc or another Class
        self.name = name
        self.parent = parent
        self.superclass_string = superclass_string if superclass_string else ''
        self.docstring = docstring
        self.body = body
        self.global_index = global_index
        self.global_index.add(self)
        self.summary = ''
        self.details = ''
        self.methods = {}
        self.properties = {}
        self.class_attributes = {}
        self.parse_class()

    @property
    def url(self):
        return self.parent.url + '#' + self.name

    def parse_class(self):
        # Parse superclasses
        def re_type_sub(match):
            return parse_type_string(match['content'], self.parent)
        super_classes = []
        for superclass in self.superclass_string.split(', '):
            super_classes.append(
                parse_type_and_add_code_tags(superclass, self))
        self.superclass_string = ', '.join(super_classes)

        # Extract summary and details
        if '\n\n' in self.docstring:
            self.summary, self.details = self.docstring.split('\n\n', 1)
        else:
            self.summary = self.docstring
            self.details = ''

        # Match remaining docstrings with property/attrs/methods
        docstrings = list(re.finditer(ClassDoc.docstring_re, self.body))
        methods = list(re.finditer(ClassDoc.method_re, self.body))
        attributes = list(re.finditer(ClassDoc.attribute_re, self.body))
        setter_decorators = list(re.finditer(ClassDoc.setter_re, self.body))
        names_with_setters = set(setter.group('name') for setter in setter_decorators)
        for docstring in docstrings:
            last_line_end_i = previous_line_ending_index_from(
                docstring.start(0), self.body)
            docstring_content = docstring.group('content')
            method_match = first_or_none(
                m for m in methods
                if m.end(0) - 1 == last_line_end_i)
            attribute_match = first_or_none(
                a for a in attributes
                if a.end(0) - 1 == last_line_end_i)
            if method_match:
                # Determine what type of method/property this is
                line_before_method = whole_line_at(method_match.start(0) - 1, self.body)
                if ClassDoc.property_re.search(line_before_method):
                    self.properties[method_match.group('method')] = AttributeDoc(
                        method_match.group('method'),
                        self,
                        docstring_content,
                        True,
                        method_match.group('method') not in names_with_setters,
                        None,
                        self.global_index)
                else:
                    if ClassDoc.staticmethod_re.search(line_before_method):
                        method_type = MethodType.staticmethod
                    elif ClassDoc.classmethod_re.search(line_before_method):
                        method_type = MethodType.classmethod
                    else:
                        method_type = MethodType.normal
                    self.methods[method_match.group('method')] = MethodDoc(
                        method_match.group('method'),
                        self,
                        method_match.group('args'),
                        docstring_content,
                        method_type,
                        self.global_index)
            elif attribute_match:
                self.class_attributes[attribute_match.group('name')] = AttributeDoc(
                    attribute_match.group('name'),
                    self,
                    docstring_content,
                    False,
                    True,
                    attribute_match.group('value'),
                    self.global_index)
            else:
                # Orphan docstring, append to class details body.
                self.details += '\n\n' + docstring_content
        self.summary = parse_general_text(self.summary, self.parent)
        self.details = parse_general_text(self.details, self.parent)
