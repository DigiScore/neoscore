from doc.utils import package_path_to_import_name


class PackageDoc:
    """A Python package as far as docs are concerned."""
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.parent_package = None
        self.subpackages = {}
        self.modules = {}

    def document():
        pass
