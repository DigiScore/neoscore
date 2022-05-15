from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.rich_text import RichText
from neoscore.core.units import Mm

neoscore.setup()

text = """
<p>
test paragraph 1
</p>
<p align=right>
test paragraph 2, aligned right!
and <span style="color: red">with coloring</span>!
</p>
"""

rt = RichText((Mm(0), Mm(0)), None, text, Mm(80))

render_example("rich_text")
