"""All custom exceptions used throughout neoscore."""


from typing import Optional


class MusicFontMetadataNotFoundError(Exception):
    """Exception raised when metadata for a music font can't be found."""


class MusicFontGlyphNotFoundError(Exception):
    """Exception raised when a glyph cannot be found in a MusicFont"""

    def __init__(self, glyph_name: str, alternate_number: Optional[int]):
        if alternate_number is None:
            self.message = f"Cannot find glyph '{glyph_name}'"
        else:
            self.message = f"Cannot find glyph '{glyph_name} [alt {alternate_number}]'"
        super().__init__(self.message)


class NoClefError(Exception):
    """Exception raised when no clef is present in a Staff where needed"""


class NoAncestorStaffError(Exception):
    """Exception raised when a StaffObject does not have an ancestor Staff"""


class DynamicStringError(Exception):

    """Exception raised when a dynamic string cannot be parsed."""

    def __init__(self, string, character):
        self.message = (
            'Cannot parse dynamic string "{}" - character "{}" unknown.'
        ).format(string, character)
        super().__init__(self.message)


class NoFlagNeededError(Exception):
    """Exception raised when a Flag is created with a non-flaggable duration"""

    def __init__(self, duration):
        self.message = "Cannot create a flag for {}".format(duration)
        super().__init__(self.message)


class FontRegistrationError(Exception):
    """Exception raised when a font is loaded from disk unsuccessfully."""

    def __init__(self, font_file_path, detail=None):
        """
        Args:
            font_file_path (str): The path to the font file which could
                not be registered.
            detail (str): Optional error details.
        """
        self.message = "Could not register font from file '{}'.{}".format(
            font_file_path, " " + detail if detail else ""
        )
        super().__init__(self.message)


class UnknownFontFamilyError(Exception):
    """
    Exception raised when an invalid font name is passed to a FontInterface.
    """


class ColorBoundsError(Exception):
    """Exception raised when a color channel is set out of bounds"""

    def __init__(self, value: int):
        self.message = f"Invalid color channel value {value}"
        super().__init__(self.message)


class InvalidIntervalError(Exception):
    """An exception raised when an invalid interval specifier is used."""


class InvalidPitchDescriptionError(Exception):
    """An exception raised when an invalid pitch specifier is used."""


class InvalidImageFormatError(Exception):
    """Raised when an image format cannot be determined."""


class ImageExportError(Exception):
    """Raised when low level image export fails."""


class NoAncestorWithMusicFontError(Exception):
    """Raised when a lookup expecting to find an ancestor with a MusicFont fails."""


class ImageLoadingError(Exception):
    """Raised when an image cannot be loaded"""
