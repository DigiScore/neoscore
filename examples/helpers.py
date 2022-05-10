import os
import pathlib
import sys
import tempfile

from neoscore.core import neoscore

"""Scaffolding for example execution"""

output_dir = pathlib.Path(__file__).parent / "output"


def render_example(name: str):
    tmp_mode = "--tmp" in sys.argv
    if not output_dir.exists() and not tmp_mode:
        os.mkdir(output_dir)
    dpi = 20 if "--automated" in sys.argv else 300
    if "--image" in sys.argv:
        if tmp_mode:
            image_path = pathlib.Path(tempfile.NamedTemporaryFile(suffix=".png").name)
        else:
            image_path = output_dir / f"{name}_image.png"
        autocrop = "--autocrop" in sys.argv
        entire_scene = "--entire-scene" in sys.argv
        neoscore.render_image(
            (
                None
                if entire_scene
                else neoscore.document.pages[0].document_space_bounding_rect
            ),
            image_path,
            dpi,
            autocrop=autocrop,
        )
    elif "--pdf" in sys.argv:
        # PDF export is currently broken
        if tmp_mode:
            pdf_path = pathlib.Path(tempfile.NamedTemporaryFile(suffix=".pdf").name)
        else:
            pdf_path = output_dir / f"{name}_pdf.pdf"
        neoscore.render_pdf(pdf_path, dpi)
    else:
        display_page_geometry = "--hide-page-geometry" not in sys.argv
        neoscore.show(display_page_geometry=display_page_geometry)
