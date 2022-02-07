import os
import re

from warnings import warn


messy_whitespace_re = re.compile(r"(?<!\n)\n *")


def package_path_to_import_name(path):
    """Convert a package path to an importable package name."""
    return re.sub(r"[\/\\]", ".", path)


def module_path_to_import_name(package_path, module_filename):
    return package_path_to_import_name(package_path) + "." + module_filename[:-3]


def first_or_none(iter):
    """Return the first item in an iterable, or None if empty.

    Like next(), but instead of raising StopIteration in the empty
    case, returns None.
    """
    try:
        return next(iter)
    except StopIteration:
        return None


def line_num_at(index, string):
    return sum(1 for char in string[: index + 1] if char == "\n") + 1


def previous_line_ending_index_from(index, string):
    """Find the index of the end of the line above a point in a string.

    This will be the index of the newline character at the end of the
    previous line.

    If the given index is on the first line of the string, returns None.
    """
    for i in range(index - 1, -1, -1):
        if string[i] == "\n":
            return i
    else:
        return None


def next_line_starting_index_from(index, string):
    """Find the index of the start of the line below a point in a string.

    If the given index is on the last line of a string, returns None.
    """
    for i in range(index, len(string)):
        if string[i] == "\n":
            if i == len(string) - 1:
                # At the end of the file
                return None
            return i + 1


def whole_line_at(index, string):
    """Return the whole line of a string at a given point.

    Unless the index is on the last line of a string,
    this will always terminate with a newline.
    """
    for i in range(index - 1, -1, -1):
        if string[i] == "\n":
            start_i = i + 1
            break
    else:
        start_i = 0
    for i in range(index, len(string)):
        if string[i] == "\n":
            end_i = i + 1
            break
    else:
        end_i = len(string)
    return string[start_i:end_i]


def indentation_level_at(index, string):
    """Find the indentation level at a given point in a string."""
    line = whole_line_at(index, string)
    if len(line) == 0:
        return 0
    i = 0
    while line[i] == " ":
        i += 1
    return i


def everything_in_indentation_block(index, string):
    level = indentation_level_at(index, string)
    start_i = next_line_starting_index_from(index, string)
    current_i = start_i
    while indentation_level_at(current_i, string) >= level or string[current_i] == "\n":
        current_i = next_line_starting_index_from(current_i, string)
        if current_i is None:
            # This block goes to the end of the string
            return string[start_i:]
    return string[start_i:current_i]


def clean_whitespace(string):
    return re.sub(messy_whitespace_re, " ", string)


def resolve_name(string, context, link_style="HTML"):
    """Attempt to find the url for the symbol named in a string.

    Args:
        string: The name to resolve. This should contain only
            one name.
        context: The ClassDoc or ModuleDoc this name appears in

    PackageDocs are specified by their qualified importable names.

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
        if item.name == string and type(item).__name__ in [
            "PackageDoc",
            "ModuleDoc",
            "ClassDoc",
        ]:
            matches.append(item.url)
        if type(item).__name__ in ["MethodDoc", "AttributeDoc"]:
            if item.parent == context:
                if string.startswith("self."):
                    if item.name == string[5:]:
                        matches.append(item.url)
                if item.name == string:
                    matches.append(item.url)
            if type(item.parent).__name__ in ["ModuleDoc", "ClassDoc"]:
                if string == item.parent.name + "." + item.name:
                    matches.append(item.url)

    if matches:
        if len(matches) > 1:
            warn(
                'Multiple possible resolutions of name "{}" in context "{}".\n'
                'Possible resolutions: {}. Choosing "{}".'.format(
                    string, context.name, matches[0]
                )
            )
        if link_style == "HTML":
            return '<a href="{}">{}</a>'.format(matches[0], string)
        elif link_style == "Markdown":
            return "[{}]({})".format(string, matches[0])
        else:
            raise ValueError("Invalid link_style: " + link_style)
    else:
        return None


def resolution_or_name(string, context, link_style="HTML"):
    """Like resolve_name, but returns the input string if no match is found."""
    resolution = resolve_name(string, context, link_style)
    return resolution if resolution else string


def parse_type_string(string, context, link_style="HTML"):
    def resolve_with_context(match):
        # Replacement method with context closure
        return resolution_or_name(match[0], context, link_style)

    return re.sub(r"(?:\w|\.)+", resolve_with_context, string)


def surround_with_tag(string, tag, **kwargs):
    attributes = {
        (key[:-1] if key.endswith("_") else key): value for key, value in kwargs.items()
    }
    return "<{}{}{}>{}</{}>".format(
        tag,
        " " if kwargs else "",
        " ".join('{}="{}"'.format(key, value) for key, value in attributes.items()),
        string,
        tag,
    )


def parse_type_and_add_code_tag(string, context, link_style="HTML"):
    parsed_string = parse_type_string(string, context)
    return surround_with_tag(parsed_string, "code")


def at_line_beginning(string, index):
    if index == 0:
        return True
    for i in range(index - 1, -1, -1):
        if string[i] == "\n":
            return True
        elif string[i] == " ":
            continue
        else:
            return False
    return True


def parse_bulleted_lists(string):
    """Convert markdown style bulleted lists to HTML unordered lists.

    Nested lists are not supported.

    "Look mom I built a state machine because I don't like Sphinx!"
    """

    result_string = ""
    in_list = False
    indentation_level = None
    bullets = []
    for i, char in enumerate(string):
        if in_list:
            if at_line_beginning(string, i):
                if char == " ":
                    # Continuation of bullet point
                    bullets[-1] += char
                else:
                    if indentation_level_at(i, string) <= indentation_level:
                        if char == "*":
                            # Next bullet point
                            bullets.append("")
                        else:
                            # End of list
                            block = surround_with_tag(
                                "".join(
                                    surround_with_tag(point, "li") for point in bullets
                                ),
                                "ul",
                            )
                            result_string += block
                            result_string += char
                            bullets = []
                            in_list = False
                            indentation_level = None
                    else:
                        # Continuation of bullet point
                        bullets[-1] += char
            else:
                # Continuation of bullet point
                bullets[-1] += char
        else:
            if char == "*" and at_line_beginning(string, i):
                # Enter list
                in_list = True
                indentation_level = indentation_level_at(i, string)
                bullets.append("")
            else:
                # Normal character outside of list
                result_string += char
    if in_list and bullets:
        # List extends to the end of the string.
        result_string += surround_with_tag(
            "".join(surround_with_tag(point, "li") for point in bullets), "ul"
        )
    return result_string


def parse_italics(string):
    def replace_function(match):
        return surround_with_tag(match["content"], "i")

    return re.sub(r"\*(?P<content>\w+.*)\*", replace_function, string)


def parse_bold(string):
    def replace_function(match):
        return surround_with_tag(match["content"], "strong")

    return re.sub(r"\*\*(?P<content>\w+.*)\*\*", replace_function, string)


def parse_backtick_code(string, context):
    def replace_function(match):
        typed_code = parse_type_string(match["content"], context)
        return surround_with_tag(typed_code, "code")

    return re.sub(r"`(?P<content>.+?)`", replace_function, string, flags=re.DOTALL)


def resolve_markdown_code_names(string, context):
    def replace_function(match):
        return surround_with_tag(parse_type_string(match["content"], context), "code")

    return re.sub(
        r"<code>(?P<content>.*?)</code>", replace_function, string, flags=re.DOTALL
    )


def parse_doctest_code(string, context):
    def replace_function(match):
        without_doctest_annotations = strip_doctest_annotations(match[0])
        typed_code = parse_type_string(without_doctest_annotations, context)
        code_block = surround_with_tag(typed_code, "code", class_="python")
        pre_block = surround_with_tag(code_block, "pre")
        # Normalize whitespace
        return re.sub(r"\n(\s*)", "\n", pre_block)

    return re.sub(r">>> .*?(?:\n\n|$)", replace_function, string, flags=re.DOTALL)


def parse_general_text(string, context, split_paragraphs=True):
    """Perform common text parsing and return ready-to-go HTML.

    * Splits paragraphs separated by blank lines into <p> blocks
    * Converts bulleted lists into <ul><li> blocks
    * Converts *italic text* and **bold text** <i> and <strong> blocks.
    * Recognizes doctest/example code blocks in >>> ... style
      and surrounds them with <code> tags
    * Recognizes arbitrary code surrounded by ` marks
      and surrounds them with <code> tags
    * Attempts to resolve all names in code blocks as <a> links
      to the documentation of those names if they are brown names.
    """
    # The order of these operations matters, as the parsing
    # helper methods make a lot of assumptions.
    string = parse_bulleted_lists(string)
    string = parse_doctest_code(string, context)
    if split_paragraphs:
        paragraphs = [p for p in re.split(r"\n\n", string) if p]
        string = "".join(surround_with_tag(paragraph, "p") for paragraph in paragraphs)
    string = parse_bold(string)
    string = parse_italics(string)
    string = parse_backtick_code(string, context)
    return string


def strip_doctest_annotations(string):
    doctest_re = re.compile(r"(# )?doctest: .*?$", flags=re.MULTILINE)
    return re.sub(doctest_re, "", string)


def ensure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
