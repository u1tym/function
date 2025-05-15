from expression import Expression
from expression import ValidResult

from phrase import Phrese
from expression_primary import ExpressionPrimary
from math_power import MathPower

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class ExpressionPower(Expression):
    phrase: str = "phrase_mathmatics.csv"

    def __init__(self: Self) -> None:
        self._pri = ExpressionPrimary(self.phrase)
        self._phr = Phrese(self.phrase)

    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:
        st: int = 0

        # expression primary
        res_pri = self._pri.isValid([text[st:]])
        if res_pri == False:
            return False
        st += res_pri["size"]

        # ^
        res = self._phr.analyze(text[st:])
        if res is None or res["name"] != "PHR_OP0":
            obj = MathPower(res_pri["obj"])
            result_value: ValidResult = {
                "result": True,
                "text": text[0:st],
                "size": st,
                "obj": obj
            }
            return result_value
        st += res["size"]

        # expression power
        res_pow = self.isValid(text[st:])
        if res_pow["result"] == False:
            return False
        st += res_pow["size"]

        obj = MathPower(res_pri["obj"], res_pow["obj"])
        result_value: ValidResult = {
            "result": True,
            "text": text[0:st],
            "size":st,
            "obj": obj
        }
        return result_value
    