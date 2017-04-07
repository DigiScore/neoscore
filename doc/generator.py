import os

from jinja2 import Environment, PackageLoader

import doc.paths as paths
from doc.utils import ensure_path_exists
from doc.parser import parse_dir


def url_to_path(url):
    return os.path.join(paths.BUILD_DIR, url[1:].replace('/', os.sep))


def generate():

    packages, modules, global_index = parse_dir(paths.PACKAGE_TO_DOC)

    env = Environment(
        loader=PackageLoader('doc', 'templates'),
        autoescape=None
    )
    module_template = env.get_template('module.html')

    for item in global_index:
        if type(item).__name__ == 'ModuleDoc':
            path = url_to_path(item.url)
            ensure_path_exists(path)
            with open(path, 'w') as file:
                file.write(module_template.render(module=item))


if __name__ == '__main__':
    generate()
