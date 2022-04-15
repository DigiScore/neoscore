Getting Started
===============

Pre-requisites
--------------

Neoscore is a `Python <https://www.python.org/>`_ library, and working with it requires a basic working knowledge of using the language.

We require a minimum Python version of 3.10. If your system does not have this version (you can check with ``python --version``), you'll need to install it. We recommend following standard Python best-practices by using a dedicated `virtual environment <https://realpython.com/python-virtual-environments-a-primer/>`_ for each of your projects, and installing neoscore in those environments rather than your global Python installation.

Installation
------------

Neoscore can be installed using pip with ``pip install neoscore``.

Once installed, check your setup by running this "hello world" program!

.. rendered-example::

   from neoscore.common import *
   neoscore.setup()
   Text(ORIGIN, None, "Hello, neoscore!")
   neoscore.show()

How these docs are organized
----------------------------

These docs are broken broadly into three sections:

1. An overview of core concepts and fundamental classes
2. An overview of the pre-made primitives for conventional western-like notation (built on those fundamental classes)
3. Exhaustive API documentation generated from docstrings

We also have `a large collection of example scores <https://github.com/DigiScore/neoscore/tree/main/vtests>`_ you can check out and play around with. Depending on your learning style, you may want to start there to get a feel for the library, or you can go straight into this guide.

.. todo::

   Update link to examples once vtests are moved to examples dir
