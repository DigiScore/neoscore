# brown.managed

## High level context managing tools for easy engraving of scores under supported well-defined notation systems

`brown` currently concerns itself primarily with providing a set of low-ish level tools for creating and manipulating music notation as vector graphic primitives. In effect, it provides tools to create scores by explicitly giving coordinates and properties for virtually every glyph in the document. This inherently makes preparing large and complex scores extremely time consuming. Compared to a less permissive notation solution like GNU Lilypond, the noise-to-signal ratio is very high.

This package aims to provide managed, high-level, opinionated contexts for easily dealing with complex scores whose notation needs largely fall within well-defined conventional systems, such as typical Western classical music notation.

This is not being actively developed due to more fundamental work in progress in the main `brown` package, so it is not advised to use any of this code quite yet. Most of the code here currently is logic initially implemented in lower level `brown` primitives, but removed due to its high-level, opinionated nature.
