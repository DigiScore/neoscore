import re

from doc.utils import (indentation_level_at,
                       parse_general_text,
                       parse_type_string,
                       parse_type_and_add_code_tag,
                       surround_with_tag,
                       whole_line_at)


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

    def parse_repeating_type_block(self, block_match, arg_mode=False):

        def re_type_sub(match):
            parsed_string = parse_type_string(match['content'], self.parent)
            return surround_with_tag(parsed_string, 'code')

        def re_type_sub_add_colon(match):
            return re_type_sub(match) + ':'

        def parse_type_and_explanation(string):
            string = string.strip()
            if ':' in string:
                if arg_mode:
                    arg_name, remainder = string.split(' ', 1)
                    type_parsed_string = re.sub(r'(?P<content>.*?)\:',
                                                re_type_sub_add_colon,
                                                remainder,
                                                1)
                    recombined = arg_name + ' ' + type_parsed_string
                    return parse_general_text(
                        recombined, self.parent)
                else:
                    type_parsed_string = re.sub(r'(?P<content>.*?)\:',
                                                re_type_sub_add_colon,
                                                string,
                                                1)
                    return parse_general_text(type_parsed_string, self.parent)
            else:
                if arg_mode:
                    return string
                else:
                    return parse_type_and_add_code_tag(string, self.parent)

        if block_match.group('body') is None:
            return []
        items = []
        lines = block_match.group('body').split('\n')
        main_indentation_level = indentation_level_at(0, lines[0])
        current_item = ''
        for line in lines:
            if (indentation_level_at(0, line) == main_indentation_level
                    and current_item):
                current_item = parse_type_and_explanation(current_item)
                items.append(current_item)
                current_item = ''
            current_item += line + '\n'

        if current_item:
            current_item = parse_type_and_explanation(current_item)
            items.append(current_item)
        return items

    def resolve_names_and_parse_html(self):
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
            self.args_details = self.parse_repeating_type_block(args_block,
                                                                arg_mode=True)

        if returns_block:
            self.returns = self.parse_repeating_type_block(returns_block)

        if raises_block:
            self.raises = self.parse_repeating_type_block(raises_block)

        if warning_block:
            self.warning = warning_block.group('body')

        args = self.args_string.split(', ')
        args = [a for a in args if a not in ['cls', 'self']]
        args = ', '.join(a for a in args)
        if args:
            args = '(' + args + ')'
            args = surround_with_tag(args, 'code')
        self.args_string = args

        self.summary = parse_general_text(self.summary, self.parent)
        self.details = parse_general_text(self.details, self.parent)
        self.warning = parse_general_text(self.warning, self.parent)
        self.args_details = [parse_general_text(arg, self.parent)
                             for arg in self.args_details]
        self.returns = [parse_general_text(ret, self.parent)
                        for ret in self.returns]
        self.exceptions = [parse_general_text(e, self.parent)
                           for e in self.exceptions]
