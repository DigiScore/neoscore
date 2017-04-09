import re

import doc.doc_config as doc_config
from doc.utils import (module_path_to_import_name,
                       first_or_none,
                       previous_line_ending_index_from,
                       indentation_level_at,
                       everything_in_indentation_block,
                       parse_general_text)
from doc.attribute_doc import AttributeDoc
from doc.class_doc import ClassDoc
from doc.method_doc import MethodDoc
from doc.method_type import MethodType


class ModuleDoc:

    """A Python module as far as docs are concerned."""

    docstring_re = re.compile(
        r'(\"\"\"(?P<content>.*?)\"\"\")',
        flags=re.DOTALL)
    class_name_re_capture = r'(?P<class>[A-Z]\w*)'
    class_re = re.compile(r'^class '
                          + class_name_re_capture
                          + r'(\((?P<superclasses>.*?)\))?'
                          + r':\n',
                          flags=re.DOTALL | re.MULTILINE)
    module_level_method_re = re.compile(
        r'^def (?P<method>[a-z_][A-Za-z_0-9]*)'
        '\((?P<args>.*?)\):\n',
        flags=re.DOTALL | re.MULTILINE)
    module_level_attribute_re = re.compile(
        r'^(?P<name>\w+) = (?P<value>.*$)\n',
        flags=re.MULTILINE)

    def __init__(self, path, name, global_index):
        self.path = path
        self.name = name
        self.package = 'NOT YET KNOWN'
        self.classes = []
        self.methods = []
        self.attributes = []
        self.global_index = global_index
        self.global_index.add(self)
        self.summary = ''
        self.details = ''
        self.parse_module()

    @property
    def url(self):
        return doc_config.API + '/' + self.name.replace('.', '/') + '.html'

    @property
    def unqualified_name(self):
        if '.' in self.name:
            return self.name.split('.')[-1]
        return self.name

    def read_file_lines(self):
        file = open(self.path, 'r')
        return file.readlines()

    def parse_module(self):
        lines = self.read_file_lines()
        contents = ''.join(lines)
        class_matches = list(re.finditer(ModuleDoc.class_re,
                                         contents))
        method_matches = list(re.finditer(ModuleDoc.module_level_method_re,
                                          contents))
        attribute_matches = list(re.finditer(ModuleDoc.module_level_attribute_re,
                                             contents))
        docstring_blocks = re.finditer(ModuleDoc.docstring_re, contents)
        # TODO: This completely ignores classes/methods without docstrings
        for block_index, block in enumerate(docstring_blocks):
            last_line_end_i = previous_line_ending_index_from(
                block.start(0), contents)
            docstring = block.group('content')
            class_match = first_or_none(
                c for c in class_matches
                if c.end(0) - 1 == last_line_end_i
                # Allow a blank line before class docstring
                or c.end(0) == last_line_end_i)
            method_match = first_or_none(
                m for m in method_matches
                if m.end(0) - 1 == last_line_end_i)
            attribute_match = first_or_none(
                a for a in attribute_matches
                if a.end(0) - 1 == last_line_end_i)
            if class_match:
                class_body = everything_in_indentation_block(
                    block.end(0), contents)
                self.classes.append(ClassDoc(
                    class_match.group('class'),
                    self,
                    class_match.group('superclasses'),
                    docstring,
                    class_body,
                    self.global_index))
            elif method_match:
                self.methods.append(MethodDoc(
                    method_match.group('method'),
                    self,
                    method_match.group('args'),
                    docstring,
                    MethodType.normal,
                    self.global_index))
            elif attribute_match:
                self.attributes.append(AttributeDoc(
                    attribute_match.group('name'),
                    self,
                    docstring,
                    False,
                    True,
                    attribute_match.group('value'),
                    self.global_index))
            elif block_index == 0:
                if '\n\n' in docstring:
                    self.summary, self.details = docstring.split('\n\n', 1)
                else:
                    self.summary = docstring
                    self.details = ''
            else:
                pass

    def resolve_names_and_parse_html(self):
        self.summary = parse_general_text(self.summary, self)
        self.details = parse_general_text(self.details, self)
