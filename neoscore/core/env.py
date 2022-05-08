"""Application-wide environment variables.

Some global behavior can be switched by environment variable toggles. For example
running any neoscore program with the environment variable ``NEOSCORE_DEBUG`` to some
truthy value will enable some debugging information like Qt bounding box outlines.
"""

import os


def _resolve_bool_env_variable(var):
    value = os.environ.get(var)
    return not (value is None or value == "0" or value.lower() == "false")


HEADLESS = _resolve_bool_env_variable("NEOSCORE_HEADLESS")
"""Whether to run the Qt application in headless mode.

Set by the environment variable ``NEOSCORE_HEADLESS``.
"""


DEBUG = _resolve_bool_env_variable("NEOSCORE_DEBUG")
"""Whether debug mode is enabled.

Set by the environment variable ``NEOSCORE_DEBUG``.
"""
