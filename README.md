# neoscore

## *notation without bars*

![A score with colored blocks and squiggly lines](https://raw.githubusercontent.com/DigiScore/neoscore/main/doc/static/img/promo_image.png)
*[Example source](https://github.com/DigiScore/neoscore/blob/main/examples/promo_image.py)*

Neoscore is a Python library for creating scores without limits. While other notation software assumes scores follow a narrow set of rules, neoscore treats scores as shapes and text with as few assumptions as possible. In neoscore, staves and noteheads are just one way of writing. Its programmatic nature makes it especially useful for generative scoremaking, and it even supports experimental animation and live-coding!

## Quick Start

Neoscore requires a minimum [Python version of **3.10**](https://www.python.org/downloads/). If you don't have it you'll need to first install it, then [set up a virtual environment with it](https://realpython.com/python-virtual-environments-a-primer/). In that environment you can then install neoscore with pip  using `pip install neoscore`, after which you should be able to run this example:

```python
from neoscore.common import *
neoscore.setup()
Text(ORIGIN, None, "Hello, neoscore!")
neoscore.show()
```

## Documentation

Visit [neoscore.org](https://neoscore.org) for thorough documentation and dozens of examples. You can find more [elaborate examples in this repository here](https://github.com/DigiScore/neoscore/blob/main/examples).

