Export
======

Beyond the interactive document view launched by :obj:`.neoscore.show`, neoscore can export documents to images and PDFs with :obj:`.neoscore.render_image` and :obj:`.render_pdf`.

PDF export takes just a DPI resolution and a file path. Image export supports several additional fields including compression quality, whether to preserve transparency, and whether to automatically crop the exported image to its contents.