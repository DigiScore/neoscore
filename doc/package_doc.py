import os

from markdown import markdown

import doc.paths as paths
from doc.utils import resolve_markdown_code_names


class PackageDoc:
    """A Python package as far as docs are concerned."""

    def __init__(self, path, name, global_index):
        self.path = path
        self.name = name
        self.parent_package = None
        self.global_index = global_index
        self.global_index.add(self)
        self.details = ''
        self.subpackages = {}
        self.modules = {}

    @property
    def url(self):
        return paths.API + '/' + self.name.replace('.', '/') + '.html'

    def resolve_names_and_parse_html(self):
        readme_path = os.path.join(self.path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as file:
                file_contents = file.read()
                html_contents = markdown(file_contents)
                self.details = resolve_markdown_code_names(html_contents, self)
