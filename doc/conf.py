# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import re
import shutil
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from pathlib import Path

from bs4 import BeautifulSoup
from sphinx.ext import apidoc

DOC_ROOT_DIR = Path(__file__).parent
PROJECT_ROOT_DIR = DOC_ROOT_DIR.parent
PROJECT_SRC_DIR = PROJECT_ROOT_DIR / "neoscore"

sys.path.insert(0, str(PROJECT_SRC_DIR))
# sys.path.insert(0, str(PROJECT_SRC_DIR/'core'))
# sys.path.insert(0, str(PROJECT_SRC_DIR/'western'))
# sys.path.insert(0, str(PROJECT_SRC_DIR/'interface'))
# Needed to let Sphinx import the `interface.qt` subpackage
# sys.path.insert(0, str(PROJECT_SRC_DIR / "interface"))


# -- Project information -----------------------------------------------------

project = "neoscore"
copyright = "2022, Andrew Yoon"
author = "Andrew Yoon"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # "sphinx_autodoc_typehints"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Sphinx settings

# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html?highlight=napoleon

napoleon_include_init_with_doc = True

# Autodoc config - see:
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

# autoclass_content = "both"
autodoc_class_signature = "separated"
autodoc_typehints_format = "short"

# Workaround for https://github.com/sphinx-doc/sphinx/issues/10290
# autodoc_typehints_format doesn't work for all situation, including class properties
python_use_unqualified_type_names = True


def all_files_in_tree(extension: str):
    for root, dirs, files in os.walk(PROJECT_SRC_DIR):
        for filename in files:
            if filename.endswith(extension):
                with open(os.path.join(root, filename), "r") as f:
                    src = f.read()
                path = Path(root, filename)
                yield path, src


def autogenerate_type_alias_mapping():
    """
    Sphinx currently requires you to explicitly copy out every type alias in
    `autodoc_type_alias` to prevent it from automatically expanding them in docs. This
    is not very maintainable, so we instead automatically gather and provide the
    mappings here. For this to work, type aliases must be explicitly annotated and they
    must be provided as top-level module members.

    See https://github.com/sphinx-doc/sphinx/issues/8934
    """
    alias_re = re.compile("^(\w+): TypeAlias =", re.MULTILINE)
    result = {}
    for path, src in all_files_in_tree(".py"):
        matches = alias_re.findall(src)
        for match in matches:
            # Convert file path to module import path
            path = path.with_suffix("")
            import_path_parts = path.parts[path.parts.index("neoscore") + 1 :]
            import_path = ".".join(import_path_parts)
            full_alias_name = import_path + "." + match
            result[match] = full_alias_name
    return result


autodoc_type_aliases = autogenerate_type_alias_mapping()


def run_apidoc(_):
    template_dir = DOC_ROOT_DIR / "templates"
    modules = [
        PROJECT_SRC_DIR / "core",
        PROJECT_SRC_DIR / "western",
        PROJECT_SRC_DIR / "interface",
        PROJECT_SRC_DIR / "interface" / "qt",
    ]
    output_dir = DOC_ROOT_DIR / "_autogenerated_api_src"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    if hasattr(sys, "real_prefix"):  # Check to see if we are in a virtualenv
        # If we are, assemble the path manually
        cmd_path = os.path.abspath(os.path.join(sys.prefix, "bin", "sphinx-apidoc"))
    else:
        cmd_path = "sphinx-apidoc"
    # Note that our templates override the apidoc-provided automodule options
    # See templates/module.rst_t
    apidoc.main(
        [
            "--separate",
            "--force",
            "--no-toc",
            "-o",
            str(output_dir),
            "--templatedir",
            str(template_dir),
            str(PROJECT_SRC_DIR),
        ]
    )


def autoapi_skip_member(app, what, name, obj, skip, options):
    """Exclude all private attributes, methods, and dunder methods from Sphinx."""

    exclude = name in [
        "__weakref__",  # special-members
        "__doc__",
        "__module__",
        "__dict__",
        "__annotations__",
        "__dataclass_fields__",
        "__dataclass_params__",
        "__delattr__",
        "__match_args__",
        "__setattr__",
    ]
    return skip or exclude


"""

since sphinx seems to not auto-link type aliases, need to manually do this. i can do
this in a post-processing step running on generated HTML files. use beautifulsoup to
find unlinked references to type aliases (as enumerated now in autodoc_type_aliases),
then automatically insert links.


make the post processing function fairly modular so i can insert other post processing
steps as will likely be needed.


<span class="pre">PointDef</span>


<a class="reference internal" href="neoscore.core.positioned_object.html#neoscore.core.positioned_object.PositionedObject" title="neoscore.core.positioned_object.PositionedObject"><span class="pre">PositionedObject</span></a>
"""


def link_aliases(soup: BeautifulSoup) -> bool:
    """Insert cross-reference links to known TypeAlias names

    Returns a bool whether any modifications were made
    """
    modified = False
    for alias_short, alias_qualified in autodoc_type_aliases.items():
        linked_file_name = alias_qualified.rsplit(".", 1)[0] + ".html"
        href = linked_file_name + "#" + alias_qualified
        replacement_el = soup.new_tag(
            "a", class_="reference internal", href=href, title=alias_qualified
        )
        inner_el = soup.new_tag("span", class_="pre")
        inner_el.append(alias_short)
        replacement_el.append(inner_el)

        def search_fn(tag):
            return (
                tag.name == "span"
                and tag.get("class") == ["pre"]
                and tag.string in [alias_short, alias_qualified]
                and tag.parent.get("class") in [["n"], ["property"]]
            )

        for ref in soup.find_all(search_fn):
            modified = True
            ref.replace_with(replacement_el)
    return modified


def post_process_html(app, exception):
    # Post-processing could potentially be done more elegantly by hooking into Sphinx's
    # doc API and modifying it before HTML is written. The event for this would probably
    # be `event.doctree-resolved`.
    if exception:
        return
    target_files = []
    for doc in app.env.found_docs:
        target_files.append(Path(app.outdir) / app.builder.get_target_uri(doc))

    for html_file in target_files:
        src = html_file.read_text()
        soup = BeautifulSoup(src, "lxml")
        modified = link_aliases(soup)
        if modified:
            print(f"{html_file.name} was modified in post-processing.")
            with open(html_file, "w") as f:
                f.write(str(soup))


def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.connect("autodoc-skip-member", autoapi_skip_member)
    app.connect("build-finished", post_process_html)
