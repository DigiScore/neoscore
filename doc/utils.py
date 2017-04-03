import re


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
            break
    start_i = i
    for i in range(index, len(string)):
        if string[i] == '\n':
            break
    end_i = i + 1
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
