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
    def unit(self) -> Unit:
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
            glyph_name (str): The canonical name of the glyph
            alternate_number (int or None): A glyph alternate number

        Returns:
            None: If the glyph is not available in the font
            dict: A collection of all known metadata about the glyph

        Raises:
            MusicFontGlyphNotFoundError: If the requested glyph
                could not be found in the font.
        """
        info = {}
        if alternate_number:
            try:
                alternate = self.metadata["glyphsWithAlternates"][glyph_name][
                    "alternates"
                ][alternate_number - 1]
                info["codepoint"] = alternate["codepoint"]
                real_name = alternate["name"]
            except KeyError:
                # Alternate not found in the font
                raise MusicFontGlyphNotFoundError
        else:
            try:
                info["codepoint"] = smufl.glyph_names[glyph_name]["codepoint"]
            except KeyError:
                raise MusicFontGlyphNotFoundError
            real_name = glyph_name

        try:
            info["description"] = smufl.glyph_names[real_name]["description"]
        except KeyError:
            pass
        try:
            info["classes"] = smufl.get_glyph_classes(real_name)
        except KeyError:
            pass
        try:
            info["glyphBBox"] = self.metadata["glyphBBoxes"][real_name]
        except KeyError:
            pass
        try:
            info["alternates"] = self.metadata["glyphsWithAlternates"][real_name][
                "alternates"
            ]
        except KeyError:
            pass
        try:
            info["anchors"] = self.metadata["glyphsWithAnchors"][real_name]
        except KeyError:
            pass
        try:
            info["componentGlyphs"] = self.metadata["ligatures"][real_name][
                "componentGlyphs"
            ]
        except KeyError:
            pass
        for set_key in self.metadata["sets"].keys():
            for glyph in self.metadata["sets"][set_key]["glyphs"]:
                if glyph["alternateFor"] == real_name:
                    info["setAlternatives"] = {}
                    info["setAlternatives"][set_key] = {}
                    info["setAlternatives"][set_key]["description"] = self.metadata[
                        "sets"
                    ][set_key]["description"]
                    info["setAlternatives"][set_key]["name"] = glyph["name"]
                    info["setAlternatives"][set_key]["codepoint"] = glyph["codepoint"]
        if not info:
            raise MusicFontGlyphNotFoundError
        info["is_optional"] = real_name in self.metadata["optionalGlyphs"]
        info["canonicalName"] = real_name
        convert_all_to_unit(info, self.unit)
        return info
