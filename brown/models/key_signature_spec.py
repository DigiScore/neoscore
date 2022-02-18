from dataclasses import dataclass
from typing import Optional

from brown.models.accidental_type import AccidentalType


@dataclass(frozen=True)
class KeySignatureSpec:
    a: Optional[AccidentalType] = None
    b: Optional[AccidentalType] = None
    c: Optional[AccidentalType] = None
    d: Optional[AccidentalType] = None
    e: Optional[AccidentalType] = None
    f: Optional[AccidentalType] = None
    g: Optional[AccidentalType] = None

    major_tonic: Optional[str] = None
