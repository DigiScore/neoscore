import pathlib
import tempfile

from neoscore.common import *

img_dir = (pathlib.Path(__file__).parent / ".." / "resources").resolve()
pixmap_image_path = img_dir / "pixmap_image.png"


def test_image_end_to_end():
    neoscore.setup()

    Image(ORIGIN, None, pixmap_image_path, 2)

    out_file = tempfile.NamedTemporaryFile(suffix=".png")
    neoscore.render_image((Mm(-100), Mm(-100), Mm(100), Mm(100)), out_file.name)
