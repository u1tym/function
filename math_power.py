from math_object import MathObject

from typing import Optional
from typing import Union
from typing import Literal
from typing import Type
from typing import Self

class MathPower(MathObject):

    def __init__(self: Self, p1: Type[MathObject], op: Optional[str] = None, p2: Optional[Type[MathObject]] = None) -> None:
        self.value1 = p1
        self.value2 = p2
        self.operator = op
    
    def print(self: Self) -> None:
        pass
