from __future__ import annotations

import copy
from typing import Dict, Optional, Type

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.utils import smufl
from neoscore.utils.exceptions import (
    MusicFontGlyphNotFoundError,
    MusicFontMetadataNotFoundError)
from neoscore.utils.platforms import PlatformType, current_platform
from neoscore.utils.units import Unit, convert_all_to_unit
from neoscore.utils.rect import Rect

from neoscore.models.glyph_info import GlyphInfo

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
        """Collect and return all known metadata about a glyph.

        Args:
            glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
            alternate_number: A glyph alternate number

        Raises:
            MusicFontGlyphNotFoundError: If the requested glyph
                could not be found in the font.
        """

        # if an alt glyph get name
        if alternate_number:
            glyph_name = self._alternate_checker(glyph_name, alternate_number)

        # check if glyphname exists then get details from smufl
        _name = smufl.glyph_names.get(glyph_name)
        if _name:
            codepoint = _name['codepoint']
            description = _name['description']
            component_glyphs = None
        else:
            #  check is it ligature or optional G and get info
            (codepoint, description, component_glyphs) = self._lig_opt_checker(glyph_name)

        # if we have made it this far and populated
        # info with all other valid details
        advance_width = self.metadata['glyphAdvanceWidths'].get(glyph_name)
        convert_all_to_unit([advance_width], self.unit)

        _boundary_box_raw = (self.metadata['glyphBBoxes'].get(glyph_name))
        convert_all_to_unit(_boundary_box_raw, self.unit)
        boundary_box = self._bBox_coords_parse(_boundary_box_raw)

        # get optional anchor metadata if available
        anchors = self.metadata['glyphsWithAnchors'].get(glyph_name)

        return GlyphInfo(canonical_name=glyph_name,
                         codepoint=codepoint,
                         description=description,
                         boundary_box=boundary_box,
                         advance_width=advance_width,
                         anchors=anchors,
                         component_glyphs=component_glyphs
                         )

    # private helper functions
    def _bBox_coords_parse(self, b_box_dict: dict) -> Rect:
        """Parses the boundary box bBoxNE and bBoxSW coords
        from SMuFL metadata into BBoxCoords dataclass"""

        # parse the boundary box coords
        rect_dataclass = Rect(x=b_box_dict["bBoxNE"][0],
                              y=b_box_dict["bBoxNE"][1],
                              width=b_box_dict["bBoxSW"][0],
                              height=b_box_dict["bBoxSW"][1]
                              )

        return rect_dataclass

    def _alternate_checker(self, glyph_name: str, alternate_number: int) -> str:
        """check to see if the alternate glyph exists,
        if it does it then returns that glyph name.

        Args: glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
            alternate_number: A glyph alternate number
        """

        # check if glyphname has alternates
        _alternate = self.metadata["glyphsWithAlternates"].get(glyph_name)

        # Alternate not found in the font
        if not _alternate:
            raise MusicFontGlyphNotFoundError

        else:
            # check if valid alt number
            alt_count = len(_alternate['alternates'])

            # if the alternate_number is in range
            if alt_count >= alternate_number:
                new_glyph_name = _alternate['alternates'][alternate_number - 1]["name"]
            else:
                # Alternate number out of range
                raise MusicFontGlyphNotFoundError

        return new_glyph_name

    def _lig_opt_checker(self, glyph_name: str) -> tuple[str, str, str]:
        """check to see if the called glyph exists as a
        ligature or as an optional, if it does it then
        populate the GlyphInfo dataclass with basic info.

               Args: info: a partially populated GlyphInfo dataclass
                   glyph_name: The canonical name of the glyph, or its main version
                       if using an alternate number.
               """

        # check if glyphname is a ligature glyph
        _ligature = self.metadata['ligatures'].get(glyph_name)
        if _ligature:
            codepoint = _ligature['codepoint']
            description = _ligature['description']
            component_glyphs = _ligature['componentGlyphs']

        # else check the optional glyph list
        else:
            _optional = self.metadata['optionalGlyphs'].get(glyph_name)

            if _optional:
                codepoint = _optional['codepoint']
                description = _optional['description']
                component_glyphs = None

            # else glyphname is not registered with SMuFL
            else:
                raise MusicFontGlyphNotFoundError

        return (codepoint, description, component_glyphs)
