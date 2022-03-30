from dataclasses import dataclass

@dataclass
class GlyphInfo:
    canonical_name: str
    codepoint: int = 0
    description: str = None
    glyphAdvanceWidths: float = 0.0
    glyphBBoxes: dict = None
    glyphsWithAnchors: dict = None
    componentGlyphs: list = None
