from dataclasses import dataclass

@dataclass
class GlyphInfo:
    canonical_name: str
    codepoint: Optional[str]
    description: Optional[str]
    glyphAdvanceWidths: float = 0.0
    glyphBBoxes: dict = None
    glyphsWithAnchors: dict = None
    componentGlyphs: list = None
