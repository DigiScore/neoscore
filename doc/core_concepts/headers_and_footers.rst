Headers and Footers
===================

Neoscore has robust support for headers and footers using higher level page overlay functions. Simply assign a function to :obj:`.neoscore.document.pages.overlay_func` which takes a :obj:`.Page` and use it to create some objects.

.. rendered-example::

    # Use a smaller paper for doc example
    neoscore.document.paper = Paper(Mm(200), Mm(150), Mm(10), Mm(10), Mm(10), Mm(10))
    def overlay(page: Page):
        page_rect = page.bounding_rect
        # Draw a rectangle around the entire page
        Path.rect((page_rect.x, page_rect.y), page,
            page_rect.width, page_rect.height, Brush.no_brush())
        # And write some text
        Text(ORIGIN, page, f"some overlay text on page {page.index + 1}")

    neoscore.document.pages.overlay_func = overlay

    Text((Mm(50), Mm(50)), None, "text directly on the page")

This overlay function is then run every time a new page is created. As a reminder, :obj:`.Document` creates pages on demand whenever accessed through :obj:`.Document.pages`, so overlay functions only apply to pages created `after` they're assigned. Consequently, if you want a page overlay to apply to all pages in your document, you should assign your overlay function at the top of your script, right after calling :obj:`.neoscore.setup`. On the other hand, this can be leveraged to disable or change overlays throughout your document.

For the common use-case of a simple header and footer, neoscore provides a built-in overlay function generator with :obj:`.page_overlays.simple_header_footer`.

.. rendered-example::

    # Use a smaller paper for doc example
    neoscore.document.paper = Paper(Mm(200), Mm(150), Mm(10), Mm(10), Mm(10), Mm(10))
    # Since the first page is a right-side page, corner text will appear on the right edge
    neoscore.document.pages.overlay_func = simple_header_footer(
        "outside top - Page %page",
        "centered top",
        "outside bottom",
        "centered bottom",
    )
    Text((Mm(50), Mm(50)), None, "text directly on the page")
