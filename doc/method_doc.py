import re

from doc.utils import (indentation_level_at,
                       parse_general_text,
                       parse_type_string,
                       parse_type_and_add_code_tags,
                       surround_with_tag)


class MethodDoc:
    """A Python method as far as docs are concerned."""

    args_re = re.compile(r'^ *Args:\n(?P<body>.*?)\n(\n| *?\Z)',
                         flags=re.DOTALL | re.MULTILINE)
    returns_re = re.compile(r'^ *Returns:\s*(?P<body>.*?)\n(\n| *?\Z)',
                            flags=re.DOTALL | re.MULTILINE)
    warning_re = re.compile(r'^ *Warning:\s*(?P<body>.*?)\n(\n| *?\Z)',
                            flags=re.DOTALL | re.MULTILINE)
    raises_re = re.compile(r'^ *Raises:\n(?P<body>.*?)\n(\n| *?\Z)',
                           flags=re.DOTALL | re.MULTILINE)

    def __init__(self, name, parent, args_string, docstring, method_type,
                 global_index):
        # parent can be a ModuleDoc or Class
        self.name = name
        self.parent = parent
        self.args_string = args_string
        self.docstring = docstring
        self.method_type = method_type
        self.args = self.args_string.split(', ')
        if self.args[0] in ['self', 'cls']:
            self.args.pop(0)
        self.global_index = global_index
        self.global_index.add(self)
        self.summary = ''
        self.details = ''
        self.args_details = []
        self.returns = ''
        self.exceptions = []
        self.warning = ''
        self.parse_method()

    @property
    def url(self):
        if type(self.parent).__name__ == 'ClassDoc':
            return self.parent.url + '.' + self.name
        else:
            return self.parent.url + '#' + self.name

    def parse_method(self):

        def re_type_sub(match):
            parsed_string = parse_type_string(match['content'], self.parent)
            code_block = surround_with_tag(parsed_string, 'code')
            return surround_with_tag(code_block, 'pre')

        current_i = 0
        while (current_i < len(self.docstring)
               and self.docstring[current_i] != '\n'):
            current_i += 1
        self.summary = self.docstring[:current_i + 1]
        args_block = MethodDoc.args_re.search(self.docstring)
        returns_block = MethodDoc.returns_re.search(self.docstring)
        warning_block = MethodDoc.warning_re.search(self.docstring)
        raises_block = MethodDoc.raises_re.search(self.docstring)
        details_end = min((match.start(0)
                           for match in [args_block, returns_block,
                                         warning_block, raises_block]
                           if match),
                          default=len(self.docstring))
        self.details = self.docstring[current_i + 1: details_end]

        if args_block:
            args_lines = args_block.group('body').split('\n')
            main_indentation_level = indentation_level_at(0, args_lines[0])
            current_arg = ''
            for line in args_lines:
                if (indentation_level_at(0, line) == main_indentation_level
                        and current_arg):
                    current_arg = re.sub(r'(?P<content>)\:',
                                         re_type_sub, current_arg, 1)
                    self.args_details.append(current_arg)
                    current_arg = ''
                current_arg += line
            if current_arg:
                current_arg = re.sub(r'(?P<content>)\:',
                                     re_type_sub, current_arg, 1)
                self.args_details.append(current_arg)

        if returns_block:
            returns = returns_block.group('body')
            self.returns = re.sub(r'(?P<content>)\:',
                                  re_type_sub, returns, 1)

        if raises_block:
            exception_lines = raises_block.group('body').split('\n')
            main_indentation_level = indentation_level_at(0, exception_lines[0])
            current_exception = ''
            for line in exception_lines:
                if (indentation_level_at(0, line) == main_indentation_level
                        and current_exception):
                    current_exception = re.sub(r'(?P<content>)\:',
                                               re_type_sub, current_arg, 1)
                    self.exceptions.append(current_exception)
                    current_exception = ''
                current_exception += line
            if current_exception:
                current_exception = re.sub(r'(?P<content>)\:',
                                           re_type_sub, current_arg, 1)
                self.exceptions.append(current_exception)
        if warning_block:
            self.warning = warning_block.group('body')

        self.summary = parse_general_text(self.summary, self.parent)
        self.details = parse_general_text(self.details, self.parent)
        self.warning = parse_general_text(self.warning, self.parent)
        self.returns = parse_general_text(self.returns, self.parent)
        self.args_details = [parse_general_text(arg, self.parent)
                             for arg in self.args_details]
        self.exceptions = [parse_general_text(e, self.parent)
                           for e in self.exceptions]
