from helpers import render_vtest

from neoscore.common import *

neoscore.setup()


Text((Mm(0), Mm(0)), None, "text on first page")
Text((Mm(0), Mm(0)), neoscore.document.pages[1], "text on second page")

render_vtest("pdf")
