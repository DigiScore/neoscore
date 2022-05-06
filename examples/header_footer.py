from helpers import render_example

from neoscore.common import *
from neoscore.core import paper
from neoscore.core.simple_header_footer import simple_header_footer

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
