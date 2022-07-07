# neoscore

## *notation without bars*

![A score with colored blocks and squiggly lines](https://raw.githubusercontent.com/DigiScore/neoscore/main/doc/static/img/promo_image.png)
*[Example source](https://github.com/DigiScore/neoscore/blob/main/examples/promo_image.py)*

Neoscore is a Python library for creating scores without limits. While other notation software assumes scores follow a narrow set of rules, neoscore treats scores as shapes and text with as few assumptions as possible. In neoscore, staves and noteheads are just one way of writing. Its programmatic nature makes it especially useful for generative scoremaking, and it even supports experimental animation and live-coding!

## Quick Start

Neoscore requires a minimum [Python version of **3.7**](https://www.python.org/downloads/). If you don't have it you'll need to first install it, then [set up a virtual environment with it](https://realpython.com/python-virtual-environments-a-primer/). In that environment you can then install neoscore with pip  using `pip install neoscore`, after which you should be able to run this example:

```python
from neoscore.common import *
neoscore.setup()
Text(ORIGIN, None, "Hello, neoscore!")
neoscore.show()
```

If you have installation problems, please see [our troubleshooting guide](https://neoscore.org/community/support.html).

## [Documentation](https://neoscore.org)

Visit [neoscore.org](https://neoscore.org) for thorough documentation and dozens of examples. You can find more [elaborate examples in this repository here](https://github.com/DigiScore/neoscore/blob/main/examples).

------------------

### Credits

Neoscore was principally developed by [Andrew Yoon](https://andrewyoon.art), originally begun in 2016 at [The Recurse Center](https://www.recurse.com/) then revived and released in 2022 with substantial support from [Craig Vear](https://www.dmu.ac.uk/about-dmu/academic-staff/art-design-humanities/craig-vear/craig-vear.aspx) and the [DigiScore](https://digiscore.dmu.ac.uk/) research project. Additional support was provided by [Prashanth Thattai Ravikumar](https://github.com/prashanthtr). Many of neoscore’s design choices were informed by the excellent open source notation projects [Abjad](https://github.com/Abjad/abjad), [Lilypond](https://lilypond.org/index.html), and [MuseScore](https://github.com/musescore/MuseScore/).

The Digital Score project (DigiScore) is funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (Grant agreement No. ERC-2020-COG - 101002086).

![Logo for the European Research Council](https://raw.githubusercontent.com/DigiScore/neoscore/main/doc/static/img/erc_eu_logo.webp)

Get your name added here by getting involved!
