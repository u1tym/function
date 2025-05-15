from abc import ABC, abstractmethod

from typing import Optional
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class MathObject(ABC):

    @abstractmethod
    def print(self: Self) -> None:
        pass

    @abstractmethod
    def get_value(self: Self, var_name: Optional[str] = None, var_val: Optional[Union[int, float]] = None) -> Union[int, float]:
        pass
