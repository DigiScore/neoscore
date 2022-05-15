from helpers import render_example

from neoscore.core import neoscore, paper
from neoscore.core.flowable import Flowable
from neoscore.core.page_overlays import simple_header_footer
from neoscore.core.units import Mm
from neoscore.western.staff import Staff

neoscore.setup(paper.A4.modified(gutter=Mm(10)))


neoscore.document.pages.overlay_func = simple_header_footer(
    "Page %page",
    "centered text is center-aligned",
    "corner text is corner-aligned",
    "neoscore header/footer example",
)

flowable = Flowable((Mm(0), Mm(0)), None, Mm(5000), Mm(15), Mm(5))
staff = Staff((Mm(0), Mm(0)), flowable, Mm(5000), line_spacing=Mm(1))


render_example("header_footer")
