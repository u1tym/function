from math_object import MathObject

from typing import Optional
from typing import Union
from typing import TypeAlias
from typing import Literal
from typing import Type
from typing import Self

PrimaryType = Literal["integer"]

_INTEGER: TypeAlias = Literal["integer"]
_DECIMAL: TypeAlias = Literal["decimal"]
_CONSTANT: TypeAlias = Literal["constant"]
_ADDITION: TypeAlias = Literal["addition"]
_FUNCTION: TypeAlias = Literal["function"]
_VARIABLE: TypeAlias = Literal["variable"]

class MathPrimary(MathObject):
    INTEGER: str = _INTEGER
    DECIMAL: str = _DECIMAL
    CONSTANT: str = _CONSTANT
    ADDITION: str = _ADDITION
    FUNCTION: str = _FUNCTION
    VARIABLE: str = _VARIABLE
    
    def __init__(self: Self,
                 typ: Literal[_INTEGER, _DECIMAL, _CONSTANT, _ADDITION, _FUNCTION, _VARIABLE],
                 obj: Type[MathObject]) -> None:
        self.typ = typ
        self.value = 1
    
    def print(self: Self) -> None:
        pass
