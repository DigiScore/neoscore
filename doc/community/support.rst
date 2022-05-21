Support
=======

Troubleshooting
---------------

.. _installation troubleshooting:

Mac OS Installation errors
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have trouble installing on Mac OS, try first upgrading your environment's pip with::

    pip install --upgrade pip

and try installing neoscore again. This should fix many problems.

PyQt5 installation problems
"""""""""""""""""""""""""""

If you see an error like this::

    AttributeError: module 'sipbuild.api' has no attribute 'prepare_metadata_for_build_wheel'

It's an upstream PyQt bug issue especially affecting new Mac M1 chips. First be sure to upgrade pip as described above. If the problem persists, `try running within the M1 compatibility layer Rosetta as described here <https://stackoverflow.com/questions/68317410/how-to-install-pyqt5-on-macos/70262165#70262165>`_.

Pillow installation problems
""""""""""""""""""""""""""""

Some versions of Mac OS have trouble installing one of our dependencies, `Pillow <https://python-pillow.org/>`_. If your installation fails, try running these commands in your environment::

    pip uninstall Pillow
    pip install --upgrade Pillow --no-binary :all:

Other Python Errors
^^^^^^^^^^^^^^^^^^^

If you're getting errors saying neoscore isn't installed or other strange Python errors, confirm that you are running on Python 3.10, the minimum required version, with ``python --version``. If you don't have it, `you'll need to install it <https://www.python.org/downloads/>`_. We strongly recommend `using a dedicated virtual environment <https://realpython.com/python-virtual-environments-a-primer/>`_ for each of your projects using neoscore.

Bug Reports
-----------

We track bugs and known feature gaps at `our issue tracker <https://github.com/DigiScore/neoscore/issues>`_. If you think you've encountered a bug, please let us know by opening an issue! But please be sure to check for neoscore updates first (`pip install --upgrade neoscore`) in case we've already fixed it, and otherwise try to find if the bug has already been reported.

Please also consider opening an issue or posting in our forum if any part of these docs were confusing or difficult for you. If you've found a typo in these docs please feel free to directly open a pull request to fix it!

