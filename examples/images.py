import pathlib

from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.image import Image
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm

neoscore.setup()

resources_dir = (pathlib.Path(__file__).parent / ".." / "tests" / "resources").resolve()
pixmap_path = resources_dir / "pixmap_image.png"
svg_path = resources_dir / "svg_image.svg"


Image(ORIGIN, None, pixmap_path, 2)

Image((Mm(10), Mm(10)), None, svg_path, 2)

Image((Mm(100), Mm(200)), None, svg_path, rotation=180)


render_example("images")
