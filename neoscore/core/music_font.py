from __future__ import annotations

import copy
from typing import Dict, Optional, Type

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.utils import smufl
from neoscore.utils.exceptions import (
    MusicFontGlyphNotFoundError,
    MusicFontMetadataNotFoundError,
)
from neoscore.utils.platforms import PlatformType, current_platform
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
        self, family_name: Optional[str] = None, unit: Optiona[Type[Unit]] = None
    ) -> MusicFont:
        return MusicFont(
            family_name if family_name is not None else self.family_name,
            unit if unit is not None else self.unit,
        )

    def glyph_info(
        self, glyph_name: str, alternate_number: Optional[int] = None
    ) -> Dict:
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
    ) -> Dict:
        """Collect and return all known metadata about a glyph.

        Args:
            glyph_name: The canonical name of the glyph, or its main version
                if using an alternate number.
            alternate_number: A glyph alternate number

        Raises:
            MusicFontGlyphNotFoundError: If the requested glyph
                could not be found in the font.
        """

        # spell out every key in metadata dict
        main_glyph_keys = ['glyphAdvanceWidths',
                           'glyphBBoxes',
                           'glyphsWithAnchors'
                           ]

        # reset the info dict
        info = {}

        # if an alt glyph get name
        if alternate_number:
            glyph_name = self._alternate_checker(glyph_name, alternate_number)

        # check existance and get details from smufl
        _name = smufl.glyph_names.get(glyph_name)

        if _name:
            info["codepoint"] = _name['codepoint']
            info["description"] = _name['description']

        # final check is it ligature or optional G
        else:
            # _ligature = dict((k, v) for k, v in self.metadata['ligatures'].items() if k == glyph_name)
            _ligature = self.metadata['ligatures'].get(glyph_name)
            if _ligature:
                # print("ligature")
                info["codepoint"] = _ligature['codepoint']
                info["componentGlyphs"] = _ligature['componentGlyphs']
                info['description'] = _ligature['description']
            # else check optional glyphs
            else:
                _optional = dict((k, v) for k, v in self.metadata['optionalGlyphs'].items() if k == glyph_name)
                _optional = self.metadata['optionalGlyphs'].get(glyph_name)

                if _optional:
                    # print("optional")
                    info["codepoint"] = _optional['codepoint']
                    info['description'] = _optional['description']
                else:
                    raise MusicFontGlyphNotFoundError

        # if we have made it this far and populated info dict then get other details
        if info:
            # fill dict with info
            for k in main_glyph_keys:
                try:
                    result = self.metadata[k][glyph_name]
                except KeyError:
                    result = []
                info[k] = result
            info['canonical_name'] = glyph_name
        else:
            raise MusicFontGlyphNotFoundError

        return info

    def _alternate_checker(self, glyph_name, alternate_number):
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

            # if the alternate_number out of range?
            if alt_count >= alternate_number:
                new_glyph_name = _alternate['alternates'][alternate_number - 1]["name"]
            else:
                # Alternate not found in the font
                # error = True
                raise MusicFontGlyphNotFoundError

        return new_glyph_name


    # def _glyph_info(
    #     self, glyph_name: str, alternate_number: Optional[int] = None
    # ) -> Dict:
    #     """Collect and return all known metadata about a glyph.
    #
    #     Args:
    #         glyph_name: The canonical name of the glyph, or its main version
    #             if using an alternate number.
    #         alternate_number: A glyph alternate number
    #
    #     Raises:
    #         MusicFontGlyphNotFoundError: If the requested glyph
    #             could not be found in the font.
    #     """
    #     # TODO LOW this is really complicated and inefficient and
    #     # doesn't furnish metadata correctly on optional glyphs and
    #     # ligatures. Refactor and test more.
    #     info = {}
    #     if alternate_number:
    #         try:
    #             alternate = self.metadata["glyphsWithAlternates"][glyph_name][
    #                 "alternates"
    #             ][alternate_number - 1]
    #             info["codepoint"] = alternate["codepoint"]
    #             canonical_name = alternate["name"]
    #         except KeyError:
    #             # Alternate not found in the font
    #             raise MusicFontGlyphNotFoundError
    #     else:
    #         try:
    #             info["codepoint"] = smufl.glyph_names[glyph_name]["codepoint"]
    #         except KeyError:
    #             try:
    #                 info["codepoint"] = self.metadata["optionalGlyphs"][glyph_name][
    #                     "codepoint"
    #                 ]
    #             except KeyError:
    #                 try:
    #                     info["codepoint"] = self.metadata["ligatures"][glyph_name][
    #                         "codepoint"
    #                     ]
    #                 except KeyError:
    #                     raise MusicFontGlyphNotFoundError
    #         canonical_name = glyph_name
    #
    #     try:
    #         info["description"] = smufl.glyph_names[canonical_name]["description"]
    #     except KeyError:
    #         pass
    #     try:
    #         info["classes"] = smufl.get_glyph_classes(canonical_name)
    #     except KeyError:
    #         pass
    #     try:
    #         info["glyphBBox"] = self.metadata["glyphBBoxes"][canonical_name]
    #     except KeyError:
    #         pass
    #     try:
    #         info["alternates"] = self.metadata["glyphsWithAlternates"][canonical_name][
    #             "alternates"
    #         ]
    #     except KeyError:
    #         pass
    #     try:
    #         info["anchors"] = self.metadata["glyphsWithAnchors"][canonical_name]
    #     except KeyError:
    #         pass
    #     try:
    #         info["componentGlyphs"] = self.metadata["ligatures"][canonical_name][
    #             "componentGlyphs"
    #         ]
    #     except KeyError:
    #         pass
    #     for set_key in self.metadata["sets"].keys():
    #         for glyph in self.metadata["sets"][set_key]["glyphs"]:
    #             if glyph["alternateFor"] == canonical_name:
    #                 info["setAlternatives"] = {}
    #                 info["setAlternatives"][set_key] = {}
    #                 info["setAlternatives"][set_key]["description"] = self.metadata[
    #                     "sets"
    #                 ][set_key]["description"]
    #                 info["setAlternatives"][set_key]["name"] = glyph["name"]
    #                 info["setAlternatives"][set_key]["codepoint"] = glyph["codepoint"]
    #     if not info:
    #         raise MusicFontGlyphNotFoundError
    #     info["canonicalName"] = canonical_name
    #     convert_all_to_unit(info, self.unit)
    #     return info
