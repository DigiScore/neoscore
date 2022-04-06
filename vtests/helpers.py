import os
import sys
import tempfile

from neoscore.core import neoscore
from neoscore.core.units import ZERO, Inch


def render_vtest(name: str):
    if "--image" in sys.argv:
        if "--tmp" in sys.argv:
            image_path = tempfile.NamedTemporaryFile(suffix=".png").name
        else:
            image_path = os.path.join(
                os.path.dirname(__file__), "output", f"{name}_image.png"
            )
        neoscore.render_image((ZERO, ZERO, Inch(2), Inch(2)), image_path)

    elif "--pdf" in sys.argv:
        # PDF export is currently broken
        pdf_path = os.path.join(os.path.dirname(__file__), "output", f"{name}_pdf.pdf")
        neoscore.render_pdf(pdf_path)
    else:
        neoscore.show()
