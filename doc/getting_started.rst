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
  
