from __future__ import annotations

import copy
from typing import Dict, Optional, Type

from neoscore.core import neoscore, smufl
from neoscore.core.exceptions import (
    MusicFontGlyphNotFoundError,
    MusicFontMetadataNotFoundError,
)
from neoscore.core.font import Font
from neoscore.core.glyph_info import GlyphInfo
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Mm, Unit, convert_all_to_unit


class MusicFont(Font):

    """A SMuFL compliant music font"""

    def __init__(self, family_name: str, unit: Type[Unit]):
        """
        Args:
            family_name: The font name
            unit: A sizing unit, where ``unit(1)`` is the distance
                between two staff lines.
        """
        self._unit = unit
        try:
            self.metadata = neoscore.registered_music_fonts[family_name]
        except KeyError:
            raise MusicFontMetadataNotFoundError
        self._engraving_defaults = copy.deepcopy(self.metadata["engravingDefaults"])
        # 1 SMuFL em is the height of a 5-line staff. See:
        # w3c.github.io/smufl/latest/specification/scoring-metrics-glyph-registration.html
        self._em_size = self.unit(4)
        self._glyph_info_cache = {}
        # engraving_defaults is small, so eagerly converting it to self.unit is ok
        convert_all_to_unit(self._engraving_defaults, self.unit)
        super().__init__(family_name, self._em_size, 1, False)

    def __str__(self):
        unit_val_as_mm = Mm(self.unit(1)).display_value
        return f"MusicFont('{self.family_name}', <unit(1) = Mm({unit_val_as_mm})>)"

    ######## PUBLIC PROPERTIES ########

    @property
    def unit(self) -> Type[Unit]:
        return self._unit

    @property
    def em_size(self) -> Unit:
        """Unit: The em size for the font."""
        return self._em_size

    @property
    def engraving_defaults(self) -> Dict:
        """dict: The SMuFL engraving defaults information for this font"""
        return self._engraving_defaults

    ######## PUBLIC METHODS ########

    def modified(
        self, family_name: Optional[str] = None, unit: Optional[Type[Unit]] = None
    ) -> MusicFont:
        return MusicFont(
            family_name if family_name is not None else self.family_name,
            unit if unit is not None else self.unit,
        )

    def glyph_info(
        self, glyph_name: str, alternate_number: Optional[int] = None
    ) -> GlyphInfo:
        """Collect and return all known metadata about a glyph.

        Args:
            glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
            alternate_number: A glyph alternate number

        Raises:
            MusicFontGlyphNotFoundError: If the requested glyph
                could not be found in the font.
        """

        key = (glyph_name, alternate_number)
        cached_result = self._glyph_info_cache.get(key, None)
        if cached_result:
            return cached_result
        computed_result = self._glyph_info(glyph_name, alternate_number)
        self._glyph_info_cache[key] = computed_result
        return computed_result

    ######## PRIVATE METHODS ########
    def _glyph_info(
        self, glyph_name: str, alternate_number: Optional[int] = None
    ) -> GlyphInfo:

        # if an alt glyph get name
        if alternate_number:
            glyph_name = self._check_alternate_names(glyph_name, alternate_number)

        # check if glyphname exists then get details from smufl
        check_name = smufl.glyph_names.get(glyph_name)
        if check_name:
            codepoint = check_name["codepoint"]
            description = check_name["description"]
        else:
            #  check is it ligature or optional glyph and get info
            (codepoint, description) = self._check_optional_glyphs(glyph_name)

        # if we have made it this far and populated
        # info with all other valid details
        advance_width = self.metadata["glyphAdvanceWidths"].get(glyph_name)
        if advance_width:
            advance_width = self.unit(advance_width)

        bounding_rect = copy.deepcopy(self.metadata["glyphBBoxes"].get(glyph_name))
        if bounding_rect:
            convert_all_to_unit(bounding_rect, self.unit)
            bounding_rect = self._convert_bbox_to_rect(bounding_rect)

        # get optional anchor metadata if available
        anchors = self._load_glyph_anchors(glyph_name)

        return GlyphInfo(
            glyph_name, codepoint, description, bounding_rect, advance_width, anchors
        )

    # private helper functions
    def _convert_bbox_to_rect(self, b_box_dict: dict) -> Rect:
        """Converst the SMuFL bounding box info
        into a Rect class format"""

        # get SMuFL bbox coords
        ne_x = b_box_dict["bBoxNE"][0]
        ne_y = b_box_dict["bBoxNE"][1]
        sw_x = b_box_dict["bBoxSW"][0]
        sw_y = b_box_dict["bBoxSW"][1]

        # calculate neoscore Rect coords
        x = sw_x
        y = ne_y * -1
        width = ne_x - sw_x
        height = ne_y - sw_y

        return Rect(x=x, y=y, width=width, height=height)

    def _check_alternate_names(self, glyph_name: str, alternate_number: int) -> str:
        """Check to see if the alternate glyph exists,
        if it does it then returns that glyph name.

        Args: glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
            alternate_number: A glyph alternate number
        """

        # check if glyphname has alternates
        alternate_glyphs = self.metadata["glyphsWithAlternates"].get(glyph_name)

        # Alternate not found in the font
        if not alternate_glyphs:
            raise MusicFontGlyphNotFoundError

        else:
            # check if valid alt number
            alt_count = len(alternate_glyphs["alternates"])

            # if the alternate_number is in range
            if alt_count >= alternate_number:
                new_glyph_name = alternate_glyphs["alternates"][alternate_number - 1][
                    "name"
                ]
            else:
                # Alternate number out of range
                raise MusicFontGlyphNotFoundError

        return new_glyph_name

    def _check_optional_glyphs(self, glyph_name: str) -> tuple[str, str]:
        """Check to see if the called glyph exists  as an optional, if it does it then
         populate the GlyphInfo dataclass with basic info.

        Args: info: a partially populated GlyphInfo dataclass
            glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
        """

        # else check the optional glyph list
        optional_glyph_field = self.metadata["optionalGlyphs"].get(glyph_name)

        if optional_glyph_field:
            codepoint = optional_glyph_field["codepoint"]

            # some don't have descriptions
            description = optional_glyph_field.get("description")

        # else glyphname is not registered with SMuFL
        else:
            raise MusicFontGlyphNotFoundError

        return (codepoint, description)

    def _load_glyph_anchors(self, glyph_name: str) -> Optional[dict[str, Point]]:
        """Load any glyph anchors and convert coordinates to neoscore points."""
        anchors = self.metadata["glyphsWithAnchors"].get(glyph_name)
        if anchors is None:
            return None
        anchors = copy.deepcopy(anchors)
        for key, value in anchors.items():
            # SMuFL coords have opposite Y axis as neoscore, so flip
            # when wrapping in Point and Unit.
            anchors[key] = Point(self.unit(value[0]), self.unit(-value[1]))
        return anchors
