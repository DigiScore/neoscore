import os

from doc.package_doc import PackageDoc
from doc.module_doc import ModuleDoc
from doc.class_doc import ClassDoc
from doc.utils import module_path_to_import_name, package_path_to_import_name


def find_in_set_by_name(search_set, name):
    return next((item for item in search_set if item.name == name),
                None)


def parse_dir(top):
    packages = set()
    modules = set()
    global_index = set()

    # Discover packages and modules
    for root, dirs, files in os.walk(top):
        if root.endswith('__pycache__') or '__init__.py' not in files:
            continue
        package_name = package_path_to_import_name(root)
        packages.add(PackageDoc(root, package_name, global_index))
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = module_path_to_import_name(root, file)
                modules.add(ModuleDoc(os.path.join(root, file),
                                      module_name, global_index))

    # Link subpackages to parent packages
    for package in packages:
        if '.' in package.name:
            parent_package_name = package.name.rsplit('.', 1)[0]
            parent_package = find_in_set_by_name(packages, parent_package_name)
            if parent_package:
                parent_package.subpackages.add(package)
                package.parent_package = parent_package

    # Link modules to packages
    for module in modules:
        if '.' in module.name:
            parent_package_name = module.name.rsplit('.', 1)[0]
            parent_package = find_in_set_by_name(packages, parent_package_name)
            if parent_package:
                parent_package.modules.add(module)
                module.package = parent_package

    for class_doc in (item for item in global_index
                      if isinstance(item, ClassDoc)):
        class_doc.resolve_superclasses()

    for doc_item in global_index:
        doc_item.resolve_names_and_parse_html()

    return packages, modules, global_index
