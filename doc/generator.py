import os
import shutil
import errno

from jinja2 import Environment, PackageLoader
from scss.compiler import Compiler as ScssCompiler

import doc.doc_config as doc_config
from doc.utils import ensure_path_exists
from doc.parser import parse_dir


def url_to_path(url):
    return os.path.join(doc_config.BUILD_DIR, url[1:].replace('/', os.sep))


def generate():

    build_root = doc_config.BUILD_DIR
    static_source_dir = os.path.join(os.path.dirname(__file__), 'static')
    js_source_dir = os.path.join(static_source_dir, 'js')
    scss_source_dir = os.path.join(static_source_dir, 'scss')
    static_build_dir = os.path.join(build_root, 'static')
    js_build_dir = os.path.join(static_build_dir, 'js')
    css_build_dir = os.path.join(static_build_dir, 'css')

    if os.path.exists(build_root):
        shutil.rmtree(build_root)

    if os.path.exists(js_source_dir):
        shutil.copytree(js_source_dir, js_build_dir)
    os.makedirs(os.path.join(doc_config.BUILD_DIR, 'static', 'css'))

    scss_compiler = ScssCompiler()
    for scss_file_name in os.listdir(scss_source_dir):
        scss_file_path = os.path.join(scss_source_dir, scss_file_name)
        with open(scss_file_path, 'r') as source:
            compiled = scss_compiler.compile_string(source.read())
            target_path = os.path.join(css_build_dir,
                                       os.path.split(scss_file_path)[1])
            if not target_path.endswith('.css'):
                target_path = os.path.splitext(target_path)[0] + '.css'
            with open(target_path, 'w') as target:
                target.write(compiled)

    packages, modules, global_index = parse_dir(doc_config.PACKAGE_TO_DOC)

    env = Environment(
        loader=PackageLoader('doc', 'templates'),
        autoescape=None
    )
    module_template = env.get_template('module.html')
    package_template = env.get_template('package.html')

    packages = [item for item in global_index
                if type(item).__name__ == 'PackageDoc']

    for item in global_index:
        if type(item).__name__ == 'ModuleDoc':
            path = url_to_path(item.url)
            ensure_path_exists(path)
            with open(path, 'w') as file:
                file.write(module_template.render(
                    module=item,
                    global_index=item.global_index,
                    packages=packages,
                    domain=doc_config.DOMAIN))
        elif type(item).__name__ == 'PackageDoc':
            path = url_to_path(item.url)
            ensure_path_exists(path)
            with open(path, 'w') as file:
                file.write(package_template.render(
                    package=item,
                    global_index=item.global_index,
                    packages=packages,
                    domain=doc_config.DOMAIN))


if __name__ == '__main__':
    generate()
