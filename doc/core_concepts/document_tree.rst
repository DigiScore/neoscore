The Document Tree
=================

Neoscore documents are organized in a `tree structure <https://en.wikipedia.org/wiki/Tree_(data_structure)>`_ where each node is represented by an object with a parent and any number of children. The root node is a :obj:`.Document`, its direct children are :obj:`.Page`\ s, and the children of pages may be any :obj:`.PositionedObject`.

.. graphviz::
   :align: center

   digraph g{
       bgcolor="transparent"
       node [shape=box];
       Document;
       {rank=same; p1; p2; p3}
       p1 [label="Page"];
       p2 [label="Page"];
       p3 [label="..."];
       Document -> p1;
       Document -> p2;
       Document -> p3;
       {rank=same; o1; o2; o3}
       o1 [label="PositionedObject"];
       o2 [label="PositionedObject"];
       o3 [label="..."];
       p2 -> o1
       p2 -> o2
       p2 -> o3
   }

The document and its pages are automatically managed through the global :obj:`neoscore.core.neoscore` module. Every neoscore program should begin by importing this module and calling the setup function, which initializes the environment including the root :obj:`.Document` object::

  from neoscore.core import neoscore
  neoscore.setup()


.. note::

   You can also use ``from neoscore.common import *`` to import the library's most commonly used modules and classes all at once, but `this is considered bad practice <https://stackoverflow.com/questions/2386714/why-is-import-bad>`_ outside of prototypes and live-coding situations.

Parents and Coordinates
-----------------------

Every object has a 2D **position** in the document, and this position is always measured relative to the object's parent. In neoscore coordinates, the X-axis increases to the right and the Y-axis increases downward. Every object must be given a parent when created; for convenience ``parent=None`` may be given as a shorthand for the first page. Coordinates are expressed in :obj:`units <neoscore.core.units>`, typically in 2D :obj:`.Point`\ s, which can usually be given as ``(x, y)`` tuples.

.. rendered-example::

   from neoscore.core import neoscore
   from neoscore.core.text import Text
   from neoscore.core.units import Mm
   neoscore.setup()
   # text_1 is given parent None, implicitly the first page,
   # and positioned at the page origin (0, 0)
   text_1 = Text((Mm(0), Mm(0)), None, "text 1")
   # text_2 is given text_1 as its parent, so its position is relative to text_1
   text_2 = Text((Mm(15), Mm(30)), text_1, "text 2")
   # text_3 is given text_2 as its parent, so its positition is relative to text_2
   # Notice how text_3's position includes a negative Y value, meaning it is
   # positioned above its parent.
   text_3 = Text((Mm(5), Mm(-10)), text_2, "text 3")
   neoscore.show()


Pages
-----

Pages are stored in :obj:`neoscore.document.pages <.Document.pages>`, a list-like object which creates pages on demand. Pages are abstract rectangular areas in the global document canvas that are used in print-oriented exports. Pages have geometry defined by an associated :obj:`.Paper`; by default neoscore uses A4 paper but this can be overriden when calling :obj:`.neoscore.setup`. Through its paper type, each page has an associated size, margins, and a gutter placed on the inside edge in double-sided printing.

For many use-cases, pages and paper are not necessary. While all objects must be a child of a page, this needn't have an effect on the output. You can work in a pageless canvas by simply parenting all "root" objects to ``None``, then disabling the interactive page preview with ``neoscore.show(display_page_geometry=False)``.
