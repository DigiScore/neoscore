Support
=======

Troubleshooting
---------------

.. _installation troubleshooting:

Mac OS Installation errors
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some versions of Mac OS have trouble installing one of our dependencies. If your installation fails, try running these commands in your environment::

    pip uninstall Pillow
    python -m pip install --upgrade pip
    python -m pip install --upgrade Pillow --no-binary :all:

Bug Reports
-----------

We track bugs and known feature gaps at https://github.com/DigiScore/neoscore/issues. If you think you've encountered a bug, please let us know by opening an issue!

Please also consider opening an issue or posting in our forum if any part of these docs were confusing or difficult for you. If you've found a typo in these docs please feel free to directly open a pull request to fix it!

