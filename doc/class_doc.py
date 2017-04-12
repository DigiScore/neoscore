import re
from itertools import chain

from doc.attribute_doc import AttributeDoc
from doc.method_doc import MethodDoc
from doc.method_type import MethodType
from doc.utils import (previous_line_ending_index_from,
                       first_or_none,
                       whole_line_at,
                       parse_general_text,
                       surround_with_tag,
                       parse_type_and_add_code_tag,
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
        self.superclasses = []
        self.methods = []
        self.inherited_methods = []
        self.properties = []
        self.inherited_properties = []
        self.class_attributes = []
        self.inherited_class_attributes = []
        self.parse_class()

    @property
    def url(self):
        return self.parent.url + '#' + self.name

    @property
    def init_method(self):
        return next((method for method in self.methods
                     if method.name == '__init__'),
                    None)

    @property
    def normal_methods(self):
        return [method for method in self.methods
                if method.method_type == MethodType.normal
                and method.name != '__init__']

    @property
    def class_methods(self):
        return [method for method in self.methods
                if method.method_type == MethodType.classmethod
                and method.name != '__init__']

    @property
    def static_methods(self):
        return [method for method in self.methods
                if method.method_type == MethodType.staticmethod
                and method.name != '__init__']

    @property
    def inherited_init_method(self):
        return next((method for method in self.inherited_methods
                     if method.name == '__init__'),
                    None)

    @property
    def inherited_normal_methods(self):
        return [method for method in self.inherited_methods
                if method.method_type == MethodType.normal
                and method.name != '__init__']

    @property
    def inherited_class_methods(self):
        return [method for method in self.inherited_methods
                if method.method_type == MethodType.classmethod
                and method.name != '__init__']

    @property
    def inherited_static_methods(self):
        return [method for method in self.inherited_methods
                if method.method_type == MethodType.staticmethod
                and method.name != '__init__']

    @property
    def all_normal_methods(self):
        return self.normal_methods + self.inherited_normal_methods

    @property
    def all_class_methods(self):
        return self.class_methods + self.inherited_class_methods

    @property
    def all_static_methods(self):
        return self.static_methods + self.inherited_static_methods

    @property
    def all_class_attributes(self):
        return self.class_attributes + self.inherited_class_attributes

    @property
    def all_properties(self):
        return self.properties + self.inherited_properties

    def parse_class(self):
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
                    self.properties.append(AttributeDoc(
                        method_match.group('method'),
                        self,
                        docstring_content,
                        True,
                        method_match.group('method') not in names_with_setters,
                        None,
                        self.global_index))
                else:
                    if ClassDoc.staticmethod_re.search(line_before_method):
                        method_type = MethodType.staticmethod
                    elif ClassDoc.classmethod_re.search(line_before_method):
                        method_type = MethodType.classmethod
                    else:
                        method_type = MethodType.normal
                    self.methods.append(MethodDoc(
                        method_match.group('method'),
                        self,
                        method_match.group('args'),
                        docstring_content,
                        method_type,
                        self.global_index))
            elif attribute_match:
                self.class_attributes.append(AttributeDoc(
                    attribute_match.group('name'),
                    self,
                    docstring_content,
                    False,
                    True,
                    attribute_match.group('value'),
                    self.global_index))
            else:
                # Orphan docstring, append to class details body.
                self.details += '\n\n' + docstring_content

    def find_inherited_names(self):
        inherited_methods = {}
        inherited_properties = {}
        inherited_class_attributes = {}
        for superclass in self.superclasses:
            (super_inherited_methods,
             super_inherited_properties,
             super_inherited_class_attributes) = superclass.find_inherited_names()
            inherited_methods = {
                **{m.name: m for m in superclass.methods},
                **super_inherited_methods,
                **inherited_methods
            }
            inherited_properties = {
                **{p.name: p for p in superclass.properties},
                **super_inherited_properties,
                **inherited_properties
            }
            inherited_class_attributes = {
                **{a.name: a for a in superclass.class_attributes},
                **super_inherited_class_attributes,
                **inherited_class_attributes
            }
        return (inherited_methods,
                inherited_properties,
                inherited_class_attributes)

    def discover_inheritence(self):
        (inherited_methods,
         inherited_properties,
         inherited_class_attributes) = self.find_inherited_names()
        all_inherited = (list(inherited_methods.values())
                         + list(inherited_properties.values())
                         + list(inherited_class_attributes.values()))
        for inherited in all_inherited:
            if type(inherited).__name__ == 'MethodDoc':
                for method in self.methods:
                    if method.name == inherited.name:
                        method.overriden_from = inherited
                        break
                else:
                    self.inherited_methods.append(inherited)
            elif (type(inherited).__name__ == 'AttributeDoc'
                    and not inherited.is_property):
                for attribute in self.class_attributes:
                    if attribute.name == inherited.name:
                        attribute.overriden_from = inherited
                        break
                else:
                    self.inherited_class_attributes.append(inherited)
            else:
                for property in self.properties:
                    if property.name == inherited.name:
                        property.overriden_from = inherited
                        break
                else:
                    self.inherited_properties.append(inherited)

    def resolve_superclasses(self):
        for superclass_name in self.superclass_string.split(', '):
            superclass = next((item for item in self.global_index
                               if type(item).__name__ == 'ClassDoc'
                               and item.name == superclass_name),
                              None)
            if superclass:
                self.superclasses.append(superclass)

    def resolve_names_and_parse_html(self):

        self.discover_inheritence()

        # Parse superclass string
        def re_type_sub(match):
            return parse_type_string(match['content'], self.parent)
        if self.superclass_string:
            superclasses = []
            for superclass in self.superclass_string.split(', '):
                superclasses.append(
                    parse_type_and_add_code_tag(superclass, self))
            self.superclass_string = ', '.join(superclasses)

        self.summary = parse_general_text(self.summary, self.parent)
        self.details = parse_general_text(self.details, self.parent)
