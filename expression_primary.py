from expression import Expression
from expression import ValidResult

from phrase import Phrese
from expression_primary import ExpressionPrimary
from math_power import MathPower

from math_primary import MathPrimary

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class ExpressionPrimary(Expression):
    phrase: str = "phrase_mathmatics.csv"

    def __init__(self: Self) -> None:
        self._phr = Phrese(self.phrase)
    
    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:
        st: int = 0

        res = self._phr.analyze(text[st:])
        if res is None:
            return False
        
        if res["name"] == "PHR_CON":
            # 定数
            obj = MathPrimary(res["name"], res["value"])
            result_value: ValidResult = {
                "result": True,
                "text": res["text"],
                "size": len(res["text"]),
                "obj": obj
            }
            return result_value
        return False
    