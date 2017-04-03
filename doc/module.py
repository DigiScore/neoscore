import os
import re

from doc.utils import (module_path_to_import_name,
                       first_or_none,
                       previous_line_ending_index_from,
                       indentation_level_at,
                       everything_in_indentation_block)
from doc.class_doc import ClassDoc
from doc.method_doc import MethodDoc
from doc.method_type import MethodType


class Module:

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

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.package = 'NOT YET KNOWN'
        self.classes = {}
        self.methods = {}
        self.summary = ''

    def read_file_lines(self):
        file = open(self.path, 'r')
        return file.readlines()

    def parse_module(self):
        lines = self.read_file_lines()
        contents = ''.join(lines)
        class_matches = list(re.finditer(Module.class_re,
                                         contents))
        method_matches = list(re.finditer(Module.module_level_method_re,
                                          contents))
        docstring_blocks = re.finditer(Module.docstring_re, contents)
        # TODO: This completely ignores classes/methods without docstrings
        for block in docstring_blocks:
            last_line_end_i = previous_line_ending_index_from(
                block.start(0), contents)
            docstring = block.group('content')
            class_match = first_or_none(
                c for c in class_matches
                if c.end(0) - 1 == last_line_end_i
                # Allow a blank line before class docstring
                or c.end(0) - 2 == last_line_end_i)
            method_match = first_or_none(
                m for m in method_matches
                if m.end(0) - 1 == last_line_end_i)
            if class_match:
                class_body = everything_in_indentation_block(
                    block.end(0), contents)
                self.classes[class_match.group('class')] = ClassDoc(
                    class_match.group('class'),
                    self,
                    class_match.group('superclasses'),
                    docstring,
                    class_body)
            elif method_match:
                self.methods[method_match.group('method')] = MethodDoc(
                    method_match.group('method'),
                    self,
                    method_match.group('args'),
                    docstring,
                    MethodType.normal)
            else:
                if self.summary:
                    self.summary += '\n\n' + docstring
                else:
                    self.summary = docstring
