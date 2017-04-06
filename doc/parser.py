import sys
import os

from doc.package_doc import PackageDoc
from doc.module_doc import ModuleDoc
from doc.utils import module_path_to_import_name, package_path_to_import_name


def parse_dir(top):
    packages = {}
    modules = {}
    global_index = set()

    # Discover packages and modules
    for root, dirs, files in os.walk(top):
        if root.endswith('__pycache__') or '__init__.py' not in files:
            continue
        package_name = package_path_to_import_name(root)
        packages[package_name] = PackageDoc(root, package_name)
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = module_path_to_import_name(root, file)
                modules[module_name] = ModuleDoc(os.path.join(root, file),
                                                 module_name, global_index)

    # Link subpackages to parent packages
    for package_name, package in packages.items():
        parent_package_name = None
        for i in range(len(package_name) - 1, -1, -1):
            if package_name[i] == '.':
                parent_package_name = package_name[:i]
                break
        if parent_package_name:
            packages[parent_package_name].subpackages[package_name] = package
            package.parent_package = packages[parent_package_name]

    # Link modules to packages
    for module_name, module in modules.items():
        package_name = None
        for i in range(len(module_name) - 1, -1, -1):
            if module_name[i] == '.':
                package_name = module_name[:i]
                break
        if package_name:
            packages[package_name].modules[module_name] = module
            module.package = packages[package_name]

    # Perform basic parsing of all modules, in turn discovering and parsing
    # classes, modules, attributes, etc.
    for module in modules.values():
        module.parse_module()

    return packages, modules, global_index


if __name__ == '__main__':
    from pprint import pprint
    packages, modules, global_index = parse_dir(sys.argv[1])
    pprint(packages)
    pprint(modules)
