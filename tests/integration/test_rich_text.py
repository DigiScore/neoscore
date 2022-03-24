import tempfile

from neoscore.common import *


def test_rich_text_end_to_end():
    neoscore.setup()

    RichText(ORIGIN, None, "<p>test</p>", Mm(50), None, 2)

    out_file = tempfile.NamedTemporaryFile(suffix=".png")
    neoscore.render_image((Mm(-100), Mm(-100), Mm(100), Mm(100)), out_file.name)
