import os
import shutil
import sys

from jinja2 import Environment, PackageLoader
from scss.compiler import Compiler as ScssCompiler

import doc.doc_config as doc_config
from doc.class_doc import ClassDoc
from doc.module_doc import ModuleDoc
from doc.package_doc import PackageDoc
from doc.utils import (
    ensure_path_exists,
    module_path_to_import_name,
    package_path_to_import_name,
)


def find_in_set_by_name(search_set, name):
    return next((item for item in search_set if item.name == name), None)


def parse_dir(top):
    packages = set()
    modules = set()
    global_index = set()

    # Discover packages and modules
    for root, dirs, files in os.walk(top):
        if root.endswith("__pycache__") or "__init__.py" not in files:
            continue
        package_name = package_path_to_import_name(root)
        packages.add(PackageDoc(root, package_name, global_index))
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = module_path_to_import_name(root, file)
                modules.add(
                    ModuleDoc(os.path.join(root, file), module_name, global_index)
                )

    # Link subpackages to parent packages
    for package in packages:
        if "." in package.name:
            parent_package_name = package.name.rsplit(".", 1)[0]
            parent_package = find_in_set_by_name(packages, parent_package_name)
            if parent_package:
                parent_package.subpackages.add(package)
                package.parent_package = parent_package

    # Link modules to packages
    for module in modules:
        if "." in module.name:
            parent_package_name = module.name.rsplit(".", 1)[0]
            parent_package = find_in_set_by_name(packages, parent_package_name)
            if parent_package:
                parent_package.modules.add(module)
                module.package = parent_package

    for class_doc in (item for item in global_index if isinstance(item, ClassDoc)):
        class_doc.resolve_superclasses()

    for doc_item in global_index:
        doc_item.resolve_names_and_parse_html()

    return packages, modules, global_index


def make_custom_pages(build_dir):
    """Copy the `custom_pages` tree into the build root."""
    custom_pages_source_dir = os.path.join(os.path.dirname(__file__), "custom_pages")
    for item in os.listdir(custom_pages_source_dir):
        source = os.path.join(custom_pages_source_dir, item)
        target = os.path.join(build_dir, item)
        if os.path.isdir(source):
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)


def url_to_path(build_root, url):
    return os.path.join(build_root, url[1:].replace("/", os.sep))


def generate(build_dir):

    build_root = build_dir
    static_source_dir = os.path.join(os.path.dirname(__file__), "static")
    js_source_dir = os.path.join(static_source_dir, "js")
    scss_source_dir = os.path.join(static_source_dir, "scss")
    static_build_dir = os.path.join(build_root, "static")
    js_build_dir = os.path.join(static_build_dir, "js")
    css_build_dir = os.path.join(static_build_dir, "css")

    if os.path.exists(build_root):
        shutil.rmtree(build_root)

    if os.path.exists(js_source_dir):
        shutil.copytree(js_source_dir, js_build_dir)
    os.makedirs(os.path.join(build_root, "static", "css"))

    scss_compiler = ScssCompiler()
    for scss_file_name in os.listdir(scss_source_dir):
        scss_file_path = os.path.join(scss_source_dir, scss_file_name)
        with open(scss_file_path, "r") as source:
            compiled = scss_compiler.compile_string(source.read())
            target_path = os.path.join(css_build_dir, os.path.split(scss_file_path)[1])
            if not target_path.endswith(".css"):
                target_path = os.path.splitext(target_path)[0] + ".css"
            with open(target_path, "w") as target:
                target.write(compiled)

    packages, modules, global_index = parse_dir(doc_config.PACKAGE_TO_DOC)

    env = Environment(loader=PackageLoader("doc", "templates"), autoescape=None)
    module_template = env.get_template("module.html")
    package_template = env.get_template("package.html")

    packages = [item for item in global_index if type(item).__name__ == "PackageDoc"]

    for item in global_index:
        if type(item).__name__ == "ModuleDoc":
            path = url_to_path(build_root, item.url)
            ensure_path_exists(path)
            with open(path, "w") as file:
                file.write(
                    module_template.render(
                        module=item,
                        global_index=item.global_index,
                        packages=packages,
                        domain=doc_config.DOMAIN,
                        page_url=item.url,
                    )
                )
        elif type(item).__name__ == "PackageDoc":
            path = url_to_path(build_root, item.url)
            ensure_path_exists(path)
            with open(path, "w") as file:
                file.write(
                    package_template.render(
                        package=item,
                        global_index=item.global_index,
                        packages=packages,
                        domain=doc_config.DOMAIN,
                        page_url=item.url,
                    )
                )

    make_custom_pages(build_dir)


def print_help():
    print("generator.py\n" "USAGE:  python doc/generator.py [out_dir]")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        build_dir = doc_config.DEFAULT_BUILD_DIR
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["-h", "--h", "-help", "--help"]:
            print_help()
            sys.exit(0)
        build_dir = sys.argv[1]
    else:
        print_help()
        sys.exit(1)

    generate(build_dir)
