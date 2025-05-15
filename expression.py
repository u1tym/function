from abc import ABC, abstractmethod

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class ValidResult(TypedDict):
    result: bool
    text: str
    size: int
    obj: Any

class Expression(ABC):

    @abstractmethod
    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:
        pass
