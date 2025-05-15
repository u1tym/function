from math_object import MathObject

from typing import Optional
from typing import Union
from typing import TypeAlias
from typing import Literal
from typing import Type
from typing import Self

class MathFormula(MathObject):
    
    def __init__(self: Self, obj: Type[MathObject]) -> None:
        self.value = obj
    
    def print(self: Self) -> None:
        pass
