"""All custom exceptions used throughout brown."""

import os


class MusicFontMetadataNotFoundError(Exception):
    """Exception raised when metadata for a music font can't be found."""
    pass


class MusicFontGlyphNotFoundError(Exception):
    """Exception raised when a glyph cannot be found in a MusicFont"""
    pass


class NoClefError(Exception):
    """Exception raised when no clef is present in a Staff where needed"""
    pass


class OutOfBoundsError(Exception):
    """Exception raised when a point lies outside of a FlowableFrame"""
    pass


class NoAncestorStaffError(Exception):
    """Exception raised when a StaffObject does not have an ancestor Staff"""
    pass


class InvalidAccidentalTypeError(Exception):
    """Raised when a nonexistent `AccidentalType` enum name is requested."""
    pass


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
        self.message = ('Cannot create a flag for {}'.format(duration))
        super().__init__(self.message)


class FontRegistrationError(Exception):
    """Exception raised when a font is loaded from disk unsuccessfully."""

    def __init__(self, font_file_path):
        """
        Args:
            font_file_path (str): The path to the font file which could
                not be registered.
        """
        self.message = "Could not register font from file '{}'.".format(
            font_file_path)
        if not os.path.isfile(font_file_path):
            self.message += " That path doesn't seem to point to a file."
        super().__init__(self.message)


class UnknownFontFamilyError(Exception):
    """
    Exception raised when an invalid font name is passed to a FontInterface.
    """
    pass


class InvalidConfigError(Exception):
    """Exception raised when a configuration is set to something invalid."""
    pass


class ColorBoundsError(Exception):
    """Exception raised when a color channel is set out of bounds"""

    def __init__(self, channel_name, value, min_allowed=0, max_allowed=255):
        self.message = (
            "Color channel '{}' must be "
            "between {} and {} (got {}).".format(channel_name,
                                                 min_allowed,
                                                 max_allowed,
                                                 value))
        super().__init__(self.message)


class InvalidIntervalError(Exception):
    """An exception raised when an invalid interval specifier is used."""
    pass


class InvalidPitchDescriptionError(Exception):
    """An exception raised when an invalid pitch specifier is used."""
    pass
