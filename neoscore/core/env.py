import os


def _resolve_bool_env_variable(var):
    value = os.environ.get(var)
    return not (value is None or value == "0" or value.lower() == "false")


HEADLESS = _resolve_bool_env_variable("NEOSCORE_HEADLESS")
"""Whether to run the Qt application in headless mode."""


DEBUG = _resolve_bool_env_variable("NEOSCORE_DEBUG")
"""Whether debug mode is enabled"""
