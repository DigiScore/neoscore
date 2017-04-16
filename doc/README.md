# brown-notation.org site & docs generator

This is an automatic generator of [brown-notation.org](brown-notation.org).
It automatically parses the `brown` package and converts its docstrings
and readme files into an API reference, combined with a few manually
assembled HTML documents which form the non-reference component of the site.

Whenever changes are made to the upstream `brown` repository, Travis CI
has been configured to regenerate the documentation and push any changes
to the [brown-notation](https://github.com/brown-notation/brown-notation.github.io)
repository, where the site is hosted on Github Pages.

To build the documentation locally:

```sh
# Make sure you are in the repository root directory
cd brown
# Install doc requirements (you may have to use pip3 instead)
pip install -r doc/doc_requirements.txt
# Run the generator
python doc/generator.py
```

This will generate the site at `doc/build`.

To view the documentation, you'll want to serve the site locally on your machine.
I recommend [twisted](https://twistedmatrix.com/trac/) because it allows you
to rebuild the site without restarting the server (unlike `python -m http.server`):

```
pip install twisted
twistd -n web --path doc/build/
```

The site will then be available at whatever port `twistd` says the server
was started on. In my case, it goes to port `8080`, so I can view the built
site in my browser at `localhost:8080`.

## Caveats

The documentation parser was mostly built from scratch, so it makes more
than a few assumptions about how dosctrings are formatted when parsing.
The docstring style is largely based on the [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
with a few changes. Until I write up a formal specification of this project's
docstring style, suffice it to say that all docstrings should look like those
around them.
