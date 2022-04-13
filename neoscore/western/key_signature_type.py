from enum import Enum

from neoscore.western.accidental_type import AccidentalType


class KeySignatureType(Enum):
    """Common key signatures.

    Key signatures are specified as dicts between the 7 pitch letter names
    and either an ``AccidentalType`` or ``None``. They are enumerated here in
    the form ``[pitch letter][f|s]_[major|minor]``. For example:

    * c major is ``KeySignatureType.c_major``
    * f-sharp minor is ``KeySignatureType.fs_minor``
    * d-flat major is ``KeySignature.df_major``

    This enum defines the entire circle of fifths - from 0 flats to 7,
    and 0 sharps to 7.
    """

    C_MAJOR = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "e": None,
        "f": None,
        "g": None,
    }

    A_MINOR = C_MAJOR.copy()

    DF_MAJOR = {
        "a": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "c": None,
        "d": AccidentalType.FLAT,
        "e": AccidentalType.FLAT,
        "f": None,
        "g": AccidentalType.FLAT,
    }

    BF_MINOR = DF_MAJOR.copy()

    CS_MAJOR = {
        "a": AccidentalType.SHARP,
        "b": AccidentalType.SHARP,
        "c": AccidentalType.SHARP,
        "d": AccidentalType.SHARP,
        "e": AccidentalType.SHARP,
        "f": AccidentalType.SHARP,
        "g": AccidentalType.SHARP,
    }

    D_MAJOR = {
        "a": None,
        "b": None,
        "c": AccidentalType.SHARP,
        "d": None,
        "e": None,
        "f": AccidentalType.SHARP,
        "g": None,
    }

    B_MINOR = D_MAJOR.copy()

    EF_MAJOR = {
        "a": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "c": None,
        "d": None,
        "e": AccidentalType.FLAT,
        "f": None,
        "g": None,
    }

    C_MINOR = EF_MAJOR.copy()

    E_MAJOR = {
        "a": None,
        "b": None,
        "c": AccidentalType.SHARP,
        "d": AccidentalType.SHARP,
        "e": None,
        "f": AccidentalType.SHARP,
        "g": AccidentalType.SHARP,
    }

    CS_MINOR = E_MAJOR.copy()

    F_MAJOR = {
        "a": None,
        "b": AccidentalType.FLAT,
        "c": None,
        "d": None,
        "e": None,
        "f": None,
        "g": None,
    }

    D_MINOR = F_MAJOR.copy()

    GF_MAJOR = {
        "a": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "c": AccidentalType.FLAT,
        "d": AccidentalType.FLAT,
        "e": AccidentalType.FLAT,
        "f": None,
        "g": AccidentalType.FLAT,
    }

    EF_MINOR = GF_MAJOR.copy()

    FS_MAJOR = {
        "a": AccidentalType.SHARP,
        "b": None,
        "c": AccidentalType.SHARP,
        "d": AccidentalType.SHARP,
        "e": AccidentalType.SHARP,
        "f": AccidentalType.SHARP,
        "g": AccidentalType.SHARP,
    }

    DS_MINOR = FS_MAJOR.copy()

    G_MAJOR = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "e": None,
        "f": AccidentalType.SHARP,
        "g": None,
    }

    E_MINOR = G_MAJOR.copy()

    AF_MAJOR = {
        "a": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "c": None,
        "d": AccidentalType.FLAT,
        "e": AccidentalType.FLAT,
        "f": None,
        "g": None,
    }

    F_MINOR = AF_MAJOR.copy()

    A_MAJOR = {
        "a": None,
        "b": None,
        "c": AccidentalType.SHARP,
        "d": None,
        "e": None,
        "f": AccidentalType.SHARP,
        "g": AccidentalType.SHARP,
    }

    FS_MINOR = A_MAJOR.copy()

    BF_MAJOR = {
        "a": None,
        "b": AccidentalType.FLAT,
        "c": None,
        "d": None,
        "e": AccidentalType.FLAT,
        "f": None,
        "g": None,
    }

    G_MINOR = BF_MAJOR.copy()

    B_MAJOR = {
        "a": AccidentalType.SHARP,
        "b": None,
        "c": AccidentalType.SHARP,
        "d": AccidentalType.SHARP,
        "e": None,
        "f": AccidentalType.SHARP,
        "g": AccidentalType.SHARP,
    }

    GS_MINOR = B_MAJOR.copy()

    CF_MAJOR = {
        "a": AccidentalType.FLAT,
        "b": AccidentalType.FLAT,
        "c": AccidentalType.FLAT,
        "d": AccidentalType.FLAT,
        "e": AccidentalType.FLAT,
        "f": AccidentalType.FLAT,
        "g": AccidentalType.FLAT,
    }
