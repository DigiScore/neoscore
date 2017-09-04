"""File system utils"""

import os


def is_valid_file_path(path):
    """Determine if a path points to a valid location for a file.

    Returns: bool
    """
    return (os.path.isdir(os.path.dirname(os.path.abspath(path)))
            and not os.path.isdir(path))
