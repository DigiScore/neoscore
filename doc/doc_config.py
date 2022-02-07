import os

import pkg_resources

VERSION = pkg_resources.require("brown")[0].version

API = "/docs/{}/api".format(VERSION)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

DEFAULT_BUILD_DIR = os.path.join(os.path.dirname(__file__), "build")

PACKAGE_TO_DOC = os.path.join("brown")

DOMAIN = "brown-notation.org"

SOURCE_ROOT = "https://github.com/ajyoon/brown/blob/master"
