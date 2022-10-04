from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.text import Text
from neoscore.core.units import Mm

"""
To render this example to a PDF file, run `python examples/pdf.py --pdf`
This tells `render_example` to run `neoscore.render_pdf()`
instead of `neoscore.show()`. The rendered PDF file will be saved in `examples/output`
"""

neoscore.setup()


Text((Mm(0), Mm(0)), None, "text on first page")
Text((Mm(0), Mm(0)), neoscore.document.pages[1], "text on second page")

render_example("pdf")
