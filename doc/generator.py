import os

from jinja2 import Environment, PackageLoader

import doc.doc_config as doc_config
from doc.utils import ensure_path_exists
from doc.parser import parse_dir


def url_to_path(url):
    return os.path.join(doc_config.BUILD_DIR, url[1:].replace('/', os.sep))


def generate():

    packages, modules, global_index = parse_dir(doc_config.PACKAGE_TO_DOC)

    env = Environment(
        loader=PackageLoader('doc', 'templates'),
        autoescape=None
    )
    module_template = env.get_template('module.html')
    package_template = env.get_template('package.html')

    for item in global_index:
        if type(item).__name__ == 'ModuleDoc':
            path = url_to_path(item.url)
            ensure_path_exists(path)
            with open(path, 'w') as file:
                file.write(module_template.render(module=item))
        elif type(item).__name__ == 'PackageDoc':
            path = url_to_path(item.url)
            ensure_path_exists(path)
            with open(path, 'w') as file:
                file.write(package_template.render(package=item))


if __name__ == '__main__':
    generate()
