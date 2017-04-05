import re

from warnings import warn


messy_whitespace_re = re.compile(r'(?<!\n)\n *')


def package_path_to_import_name(path):
    """Convert a package path to an importable package name."""
    return re.sub(r'[\/\\]', '.', path)


def module_path_to_import_name(package_path, module_filename):
    return package_path_to_import_name(package_path) + '.' + module_filename[:-3]


def first_or_none(iter):
    """Return the first item in an iterable, or None if empty.

    Like next(), but instead of raising StopIteration in the empty
    case, returns None.
    """
    try:
        return next(iter)
    except StopIteration:
        return None


def previous_line_ending_index_from(index, string):
    """Find the index of the end of the line above a point in a string.

    If the given index is on the first line of the string, returns None.
    """
    for i in range(index - 1, -1, -1):
        if string[i] == '\n':
            return i
    else:
        return None


def next_line_starting_index_from(index, string):
    """Find the index of the start of the line below a point in a string.

    If the given index is on the last line of a string, returns None.
    """
    for i in range(index, len(string)):
        if string[i] == '\n':
            if i == len(string) - 1:
                # At the end of the file
                return None
            return i + 1


def whole_line_at(index, string):
    """Return the whole line of a string at a given point."""
    for i in range(index, -1, -1):
        if string[i] == '\n':
            start_i = i + 1
            break
    else:
        start_i = index + 1

    for i in range(index, len(string)):
        if string[i] == '\n':
            end_i = i + 1
            break
    else:
        end_i = index + 1
    return string[start_i: end_i]


def indentation_level_at(index, string):
    """Find the indentation level at a given point in a string."""
    line = whole_line_at(index, string)
    if len(line) == 0:
        return 0
    i = 0
    while line[i] == ' ':
        i += 1
    return i


def everything_in_indentation_block(index, string):
    level = indentation_level_at(index, string)
    start_i = next_line_starting_index_from(index, string)
    current_i = start_i
    while (indentation_level_at(current_i, string) > level
           or indentation_level_at(current_i, string) == 0):
        current_i = next_line_starting_index_from(current_i, string)
        if current_i is None:
            # This block goes to the end of the string
            return string[start_i:]
    return string[start_i: current_i]


def clean_whitespace(string):
    return re.sub(messy_whitespace_re, ' ', string)


def resolve_name(string, context):
    """Attempt to find the url for the symbol named in a string.

    Args:
        string: The name to resolve. This should contain only
            one name.
        context: The ClassDoc or ModuleDoc this name appears in

    Packages are specified by their qualified importable names.

    Modules are specified by their qualified importable names.

    Classes are expected to simply be specified by their names.

    * Methods/attributes in the same context may be referred to by their
      simple name.
    * Methods/attributes in classes may be referred to by self.name
    * Methods/attributes in classes are specified as ClassName.name
    * Methods/attributes at module-levels are specified as module_name.name

    If multiple resolutions can be found for the string, a warning
    will be emitted and the first found will be returned.

    Returns:
        str: The resolved url of the given name
        None: If the name could not be resolved
    """
    global_index = context.global_index

    matches = []
    for item in global_index:
        if (item.name == string and type(item).__name__ in
                ['PackageDoc', 'ModuleDoc', 'ClassDoc']):
            matches.append(item.url)
        if type(item).__name__ in ['MethodDoc', 'AttributeDoc']:
            if item.parent == context:
                if string.startswith('self.'):
                    if item.name == string[5:]:
                        matches.append(item.url)
                if item.name == string:
                    matches.append(item.url)
            if type(item.parent).__name__ in ['ModuleDoc', 'ClassDoc']:
                if string == item.parent.name + '.' + item.name:
                    matches.append(item.url)

    if matches:
        if len(matches) > 1:
            warn('Multiple possible resolutions of name "{}" in context "{}".\n'
                 'Could match: {}. Choosing "{}".'.format(string,
                                                          context.name,
                                                          matches[0]))
        return '<a href="{}">{}</a>'.format(matches[0], string)
    else:
        return None


def resolution_or_name(string, context):
    """Like resolve_name, but returns the input string if no match is found."""
    resolution = resolve_name(string, context)
    return resolution if resolution else string


def parse_type_string(string, context):

    def resolve_with_context(match):
        # Replacement method with context closure
        return resolution_or_name(match[0], context)

    return re.sub('\w+', resolve_with_context, string)
