from __future__ import annotations

import copy
from typing import Dict, Optional, Type

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.models.glyph_info import GlyphInfo
from neoscore.utils import smufl
from neoscore.utils.exceptions import (
    MusicFontGlyphNotFoundError,
    MusicFontMetadataNotFoundError,
)
from neoscore.utils.platforms import PlatformType, current_platform
from neoscore.utils.rect import Rect
from neoscore.utils.units import Unit, convert_all_to_unit

# TODO LOW make a nice __repr__


class MusicFont(Font):

    """A SMuFL compliant music font"""

    # Scaling factor which may or may not work for fonts other than Bravura.
    if current_platform() == PlatformType.MAC:
        __magic_em_scale = 4
    else:
        __magic_em_scale = 3

    def __init__(self, family_name: str, unit: Type[Unit]):
        """
        Args:
            family_name: The font name
            unit: A sizing unit, where `unit(1)` is the distance
                between two staff lines.
        """
        self._unit = unit
        try:
            self.metadata = neoscore.registered_music_fonts[family_name]
        except KeyError:
            raise MusicFontMetadataNotFoundError
        self._engraving_defaults = copy.deepcopy(self.metadata["engravingDefaults"])
        self._em_size = self.unit(self.__magic_em_scale)
        self._glyph_info_cache = {}
        # engraving_defaults is small, so eagerly converting it to self.unit is ok
        convert_all_to_unit(self._engraving_defaults, self.unit)
        super().__init__(family_name, self._em_size, 1, False)

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

    ######## SPECIAL METHODS ########

    def __eq__(self, other):
        return (
            isinstance(other, MusicFont)
            # Compare only based on name and concrete point size,
            # allowing fonts with different but equivalent `unit`
            # types to be equal.
            and self.family_name == other.family_name
            and self.size == other.size
        )

    def __hash__(self):
        return hash((self.family_name, self.size.rounded_base_value))

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
            codepoint = check_name['codepoint']
            description = check_name['description']
        else:
            #  check is it ligature or optional G and get info
            (codepoint, description) = self._check_optional_glyphs(glyph_name)

        # if we have made it this far and populated
        # info with all other valid details
        advance_width = self.metadata['glyphAdvanceWidths'].get(glyph_name)
        if advance_width:
            advance_width = self.unit(advance_width)

        bounding_box = copy.deepcopy(self.metadata['glyphBBoxes'].get(glyph_name))
        if bounding_box:
            convert_all_to_unit(bounding_box, self.unit)
            bounding_box = self._convert_bbox_to_rect(bounding_box)

        # get optional anchor metadata if available
        anchors = self.metadata['glyphsWithAnchors'].get(glyph_name)

        return GlyphInfo(canonical_name=glyph_name,
                         codepoint=codepoint,
                         description=description,
                         bounding_box=bounding_box,
                         advance_width=advance_width,
                         anchors=anchors
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
            alt_count = len(alternate_glyphs['alternates'])

            # if the alternate_number is in range
            if alt_count >= alternate_number:
                new_glyph_name = alternate_glyphs['alternates'][alternate_number - 1]["name"]
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
        optional_glyph_field = self.metadata['optionalGlyphs'].get(glyph_name)

        if optional_glyph_field:
            codepoint = optional_glyph_field['codepoint']

            # some don't have descriptions
            description = optional_glyph_field.get('description')


        # else glyphname is not registered with SMuFL
        else:
            raise MusicFontGlyphNotFoundError

        return (codepoint, description)
