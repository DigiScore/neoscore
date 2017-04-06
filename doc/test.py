import subprocess

from doc.utils import parse_general_text
from doc.parser import parse_dir


string = """

Hello world, this is a paragraph.
Just a normal one, cool.

Neat

Here is a list:
* Hello
* Multi
  line
* World

Here is some `inline code with types like Staff`

Here is some *italicized text*

Here is some **bold text**

Here is a doctest:

>>> doesnt work of
... course,
   ... but you bet your butt it normalizes whitespace
   ...                                     correctly.
... But it sure can resolve names:
... staff = Staff(Point(x, y), Mm(20))

"""

packages, modules, global_index = parse_dir('brown')
context = modules['brown.core.staff'].classes['Staff']

with open('doc/test.html', 'w') as file:
    file.write(parse_general_text(string, context))

subprocess.call(['firefox', 'doc/test.html'])
