Interactivity
=============

Neoscore has experimental support for interactive scores which can change on the fly through live coding and animation. Most properties of neoscore graphical objects are mutable (modifiable), and changing them while the interactive neoscore view is running can update their rendered representations on the fly.

Live coding with a REPL
-----------------------

You can integrate neoscore applications with a Python `REPL <https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`_ through `IPython <https://ipython.org/>`_. To get started, install ipython in your environment with ``pip install ipython``. Once installed you can run or write neoscore programs using the ipython shell with the flag ``--gui=qt5``::

    $ ipython --gui=qt5
    Python 3.10.4 (main, Mar 23 2022, 23:05:40) [GCC 11.2.0]
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.2.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from neoscore.common import *

    In [2]: neoscore.setup()

    In [3]: text = Text(ORIGIN, None, 'hello REPL!')

    In [4]: neoscore.show()

    In [5]: text.pos = (Mm(50), Mm(100))

    In [6]: text.text = 'changing text!'

You can also write starting code in a python script as usual, then run it interactively with ``ipython --gui=qt5 -i your_script.py``.

Animation
---------

You can also animate your scores by passing a callback function to :obj:`.neoscore.show`::

    from neoscore.common import *
    import math
    from typing import Optional

    neoscore.setup()
    center = Mm(50)
    text = Text((center, Mm(50)), None, "moving text")

    def refresh_func(time: float) -> Optional[neoscore.RefreshFuncResult]:
        text.x = center + Mm(math.sin(time) * 20)

    neoscore.show(refresh_func)

This callback will be automatically executed at up to 60 times per second. The refresh function is called with the current system time in seconds. Optionally, some state can be returned to the neoscore runtime with a :obj:`.neoscore.RefreshFuncResult` object, such as indicating to the runtime that no scene re-render is required.

.. note::

    You may notice dropped frames and stuttering in animated scenes. This is a limitation of neoscore's animation system with no current solution beside simplifying scenes, running at lower target framerates (see below), and running on faster hardware.

You can also change the refresh function on the fly (live-coded animations!) with :obj:`.neoscore.set_refresh_func`. This function also allows overriding the target framerate.

Caveats
-------

Interactivity currently has `many` caveats, and it is not considered guaranteed API behavior. In general, complex managed objects which automatically generate child objects do not respond well to mutation. Paths which have elements parented to other objects don't either. Which objects and properties can be mutated and how is not currently documented, so you'll have to just try things and see what works.
