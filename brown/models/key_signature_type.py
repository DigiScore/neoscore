from enum import Enum

from brown.models.accidental_type import AccidentalType

flat = AccidentalType.flat
sharp = AccidentalType.sharp


class KeySignatureType(Enum):
    """Common key signatures.

    Key signatures are specified as `dict`s between the 7 pitch letter names
    and either an `AccidentalType` or `None`. They are enumerated here in
    the form `[pitch letter][f|s]_[major|minor]`. For example:

    * c major is `KeySignatureType.c_major`
    * f-sharp minor is `KeySignatureType.fs_minor`
    * d-flat major is `KeySignature.df_major`

    This enum defines the entire circle of fifths - from 0 flats to 7,
    and 0 sharps to 7.
    """

    c_major = {
        'a': None,
        'b': None,
        'c': None,
        'd': None,
        'e': None,
        'f': None,
        'g': None,
    }

    a_minor = c_major.copy()

    df_major = {
        'a': flat,
        'b': flat,
        'c': None,
        'd': flat,
        'e': flat,
        'f': None,
        'g': flat,
    }

    bf_minor = df_major.copy()

    # Ha
    cs_major = {
        'a': sharp,
        'b': sharp,
        'c': sharp,
        'd': sharp,
        'e': sharp,
        'f': sharp,
        'g': sharp,
    }

    d_major = {
        'a': None,
        'b': None,
        'c': sharp,
        'd': None,
        'e': None,
        'f': sharp,
        'g': None,
    }

    b_minor = d_major.copy()

    ef_major = {
        'a': flat,
        'b': flat,
        'c': None,
        'd': None,
        'e': flat,
        'f': None,
        'g': None,
    }

    c_minor = ef_major.copy()

    e_major = {
        'a': None,
        'b': None,
        'c': sharp,
        'd': sharp,
        'e': None,
        'f': sharp,
        'g': sharp,
    }

    cs_minor = e_major.copy()

    f_major = {
        'a': None,
        'b': flat,
        'c': None,
        'd': None,
        'e': None,
        'f': None,
        'g': None,
    }

    d_minor = f_major.copy()

    gf_major = {
        'a': flat,
        'b': flat,
        'c': flat,
        'd': flat,
        'e': flat,
        'f': None,
        'g': flat,
    }

    ef_minor = gf_major.copy()

    fs_major = {
        'a': sharp,
        'b': None,
        'c': sharp,
        'd': sharp,
        'e': sharp,
        'f': sharp,
        'g': sharp,
    }

    ds_minor = fs_major.copy()

    g_major = {
        'a': None,
        'b': None,
        'c': None,
        'd': None,
        'e': None,
        'f': sharp,
        'g': None,
    }

    e_minor = g_major.copy()

    af_major = {
        'a': flat,
        'b': flat,
        'c': None,
        'd': flat,
        'e': flat,
        'f': None,
        'g': None,
    }

    f_minor = af_major.copy()

    a_major = {
        'a': None,
        'b': None,
        'c': sharp,
        'd': None,
        'e': None,
        'f': sharp,
        'g': sharp,
    }

    fs_minor = a_major.copy()

    bf_major = {
        'a': None,
        'b': flat,
        'c': None,
        'd': None,
        'e': flat,
        'f': None,
        'g': None,
    }

    g_minor = bf_major.copy()

    b_major = {
        'a': sharp,
        'b': None,
        'c': sharp,
        'd': sharp,
        'e': None,
        'f': sharp,
        'g': sharp,
    }

    gs_minor = b_major.copy()

    cf_major = {
        'a': flat,
        'b': flat,
        'c': flat,
        'd': flat,
        'e': flat,
        'f': flat,
        'g': flat,
    }
