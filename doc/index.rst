neoscore
========

.. role:: subtitle-slogan
   :class: subtitle-slogan

:subtitle-slogan:`notation without bars`

.. image:: _static/img/promo_image.png
  :alt: A score with colored blocks and squiggly lines
  :target: https://github.com/DigiScore/neoscore/blob/main/examples/promo_image.py

Neoscore is a Python programming library for creating scores without limits. While other notation software assumes scores follow a narrow set of rules, neoscore treats scores as shapes and text with as few assumptions as possible. In neoscore, staves and noteheads are just one way of writing.

Neoscore uses a layered architecture which allows users to work with low-level graphics primitives and higher-level notation constructs according to their needs. Users can build sophisticated scores using the substantial built-in primitives, or they can treat the library as a framework on which to build complex new notation systems. Experimentally it also supports an interactive runtime allowing users to live code on scores and even animate them.

We differ from traditional score-writing systems in many important aspects. Neoscore deliberately lacks support for things like audio playback, MusicXML, MIDI, automatic score layout, and part extraction. We treat traditional western notation as a second class citizen. In general, if your score *can* be written with traditional score-writers you're better off using one. But if your notation speaks in dots and squiggles, grids and colors, bouncing barlines and unruly clefs—you're in the right place!

.. raw:: html

   <!-- Github button -->
   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/DigiScore/neoscore" data-icon="octicon-star" data-size="large" aria-label="Star DigiScore/neoscore on GitHub">Don't forget to star us on GitHub!</a>

.. toctree::
   :hidden:

   getting_started.rst

.. toctree::
   :hidden:
   :caption: Core Concepts

   core_concepts/graphical_notation.rst
   core_concepts/document_tree.rst
   core_concepts/text_and_fonts.rst
   core_concepts/paths.rst
   core_concepts/brushes_and_pens.rst
   core_concepts/music_text.rst
   core_concepts/images.rst
   core_concepts/flowables.rst
   core_concepts/rotation_and_scaling.rst
   core_concepts/headers_and_footers.rst
   core_concepts/export.rst
   core_concepts/interactivity.rst

.. toctree::
   :hidden:
   :caption: Western Notation

   western/western.rst
   western/staff.rst
   western/notes_chords_rests.rst
   western/chordrests_advanced.rst
   western/beams.rst
   western/expressive_text.rst
   western/spanners.rst
   western/multi_staff_objects.rst
   western/tablature.rst

.. toctree::
   :hidden:
   :caption: Extending Neoscore

   extending/extending_neoscore.rst

.. toctree::
   :hidden:
   :caption: Community

   community/support.rst
   community/community.rst

.. toctree::
   :hidden:
   :caption: API Reference

   api/neoscore.core
   api/neoscore.western
   api/neoscore.interface


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
