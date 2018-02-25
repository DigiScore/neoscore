from brown.core import brown


"""The main module and interface for the gustav notation context."""


instruments = []
"""list[Instrument]: The instruments in the score.

The `Instrument`s should be given in descending order.
For example, a string quartet might be listed as:

`[Violin_I, Violin_II, Viola, Cello]`
"""


def setup(instr, paper=None):
    """Set up the `gustav` context.

    In `gustav` scores, this should be used in place of `brown.setup()`.

    Args:
        instr (list[Instrument]): The instruments in the score
        paper (Paper): The paper to use in the document.
            If `None`, this defaults to `constants.DEFAULT_PAPER_TYPE`

    Returns: None
    """
    global instruments
    brown.setup(paper)
    instruments = instr
