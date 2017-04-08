import re

from doc.utils import (indentation_level_at,
                       parse_general_text,
                       parse_type_string,
                       parse_type_and_add_code_tag,
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
        self.args = ''
        self.global_index = global_index
        self.global_index.add(self)
        self.summary = ''
        self.details = ''
        self.args_details = []
        self.returns = []
        self.exceptions = []
        self.warning = ''

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

        def re_type_sub(match):
            parsed_string = parse_type_string(match['content'], self.parent)
            return surround_with_tag(parsed_string, 'code')

        def re_type_sub_add_colon(match):
            return re_type_sub(match) + ':'

        def parse_type_and_explanation(string):
            if ':' in string:
                return re.sub(r'(?P<content>)\:',
                              re_type_sub_add_colon, string, 1)
            else:
                return parse_type_and_add_code_tag(string, self.parent)

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
                    current_arg = parse_type_and_explanation(current_arg)
                    self.args_details.append(current_arg)
                    current_arg = ''
                current_arg += line
            if current_arg:
                current_arg = parse_type_and_explanation(current_arg)
                self.args_details.append(current_arg)

        if returns_block:
            return_lines = returns_block.group('body').split('\n')
            main_indentation_level = indentation_level_at(0, return_lines[0])
            current_return = ''
            for line in return_lines:
                if (indentation_level_at(0, line) == main_indentation_level
                        and current_return):
                    current_return = parse_type_and_explanation(current_return)
                    self.returns.append(current_return)
                    current_return = ''
                current_return += line
            if current_return:
                current_return = parse_type_and_explanation(current_return)
                self.returns.append(current_return)

        if raises_block:
            exception_lines = raises_block.group('body').split('\n')
            main_indentation_level = indentation_level_at(0, exception_lines[0])
            current_exception = ''
            for line in exception_lines:
                if (indentation_level_at(0, line) == main_indentation_level
                        and current_exception):
                    current_exception = parse_type_and_explanation(current_exception)
                    self.exceptions.append(current_exception)
                    current_exception = ''
                current_exception += line
            if current_exception:
                current_exception = parse_type_and_explanation(current_exception)
                self.exceptions.append(current_exception)

        if warning_block:
            self.warning = warning_block.group('body')

        args = self.args_string.split(', ')
        args = [a for a in args if a not in ['cls', 'self']]
        args = ', '.join(a for a in args)
        self.args_string = surround_with_tag(args, 'code')

        self.summary = parse_general_text(self.summary, self.parent)
        self.details = parse_general_text(self.details, self.parent)
        self.warning = parse_general_text(self.warning, self.parent)
        if any(arg is None for arg in self.args_details):
            import pdb;pdb.set_trace()
        self.args_details = [parse_general_text(arg, self.parent)
                             for arg in self.args_details]
        self.exceptions = [parse_general_text(e, self.parent)
                           for e in self.exceptions]
