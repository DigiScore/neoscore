from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.text import Text
from neoscore.core.units import Mm

neoscore.setup()


Text((Mm(0), Mm(0)), None, "text on first page")
Text((Mm(0), Mm(0)), neoscore.document.pages[1], "text on second page")

render_example("pdf")
