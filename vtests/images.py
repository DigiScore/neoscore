import pathlib

from helpers import render_vtest

from neoscore.common import *

resources_dir = (pathlib.Path(__file__).parent / ".." / "tests" / "resources").resolve()

neoscore.setup()


Image(ORIGIN, None, resources_dir / "pixmap_image.png", 2)

Image((Mm(10), Mm(10)), None, resources_dir / "svg_image.svg", 2)

render_vtest("images")
