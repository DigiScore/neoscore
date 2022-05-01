Extending Neoscore
==================

We've now completed our overview of neoscore's built-in functionality! Neoscore offers considerable functionality out of the box, and you can get quite a lot done just using the built-in classes, but for many use-cases its true power is in offering a framework upon which to build your own notation systems. In this section we will discuss the architectural principles behind the library and work through a couple examples for how to build on top of neoscore.

Architecture
------------

Neoscore's core functionality is divided into 3 main components: the :obj:`.core` module discussed earlier, a Qt backend for graphics rendering, and an :obj:`.interface` layer translating between the two. Extensions, including ``western``, mostly integrate with the ``core`` module, but may occasionally need to manipulate interface classes directly. Communication between these architectural layers is generally one directional: ``core`` talks to ``interface``, but ``interface`` doesn't talk back. You should almost never need to deal with the Qt layer directly.

.. graphviz::
   :align: center

   digraph g{
       bgcolor="transparent"
       node [shape=box];
       {rank=same; 2; 3; 4; 5}
       1 [label = "extensions"];
       2 [label = "western"];
       3 [label = "core"];
       4 [label = "interface"];
       5 [label = "Qt via PyQt5"];
       1 -> 2
       1 -> 3
       1 -> 4 [style=dotted]
       2 -> 3
       3 -> 4
       4 -> 5
   }

The :obj:`.interface` layer provides low-level representations of core-layer objects. The document tree at the interface layer is completely flattened; every interface object is positioned in absolute document coordinates. Interface classes are also immutable; once created they cannot be changed. Mutation in interactive contexts like animation and live-coding is achieved by continually destroying and recreating interface classes.

.. note::

   For those more familiar with GUI systems, Neoscore's interactive runtime acts essentially like an immediate-mode GUI. This is despite the fact that Qt is a retained-mode framework, and that discrepancy is why animations can't run smoothly. Eventually we would like to migrate to something like `imgui <https://github.com/ocornut/imgui>`_ to resolve this. There are no technical hurdles to this that we know of, just time constraints. If you want to take a shot at this, get in touch!

Rendering
---------

When a neoscore document is rendered, an initial :obj:`.Document.render` call is dispatched which fans out :obj:`.PositionedObject.render` calls throughout the document tree depth-first. Each class's ``render`` implementation is responsible for creating any backing ``interface`` classes.

For objects in flowable containers, :obj:`.PositionedObject.render` delegates to the :obj:`.PositionedObject.render_in_flowable` method. This method looks at the object's position in the flowable and determines, according to its :obj:`breakable_length <.PositionedObject.breakable_length>`, which flowable lines it appears on. If the object fits entirely into its first line, it calls :obj:`render_complete <.PositionedObject.render_complete>`. Otherwise it calls :obj:`render_before_break <.PositionedObject.render_before_break>` once at the first line, :obj:`render_after_break <.PositionedObject.render_after_break>` once at the last line, and :obj:`render_spanning_continuation <.PositionedObject.render_spanning_continuation>` once for each full line in between.

Each of these methods can be overridden by custom classes to create custom rendering behavior.

You can also implement :obj:`.PositionedObject.pre_commit_hook` and :obj:`.PositionedObject.post_commit_hook` to run code immediately before and after document rendering occurs. This is primarily useful for pre-computing expensive properties before rendering.

