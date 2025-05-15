from expression import Expression
from expression import ValidResult

from phrase import Phrese
from expression_power import ExpressionPower
from math_multiplicative import MathMultiplicative

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class ExpressionMultiplicative(Expression):
    phrase: str = "phrase_mathmatics.csv"

    def __init__(self: Self) -> None:
        self._pow = ExpressionPower(self.phrase)
        self._phr = Phrese(self.phrase)

    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:
        st: int = 0

        # expression power
        res_pow = self._pow.isValid(text[st:])
        if res_pow == False:
            return False
        st += res_pow["size"]

        # */
        res = self._phr.analyze(text[st:])
        if res is None:
            obj = MathMultiplicative(res_pow["obj"])
            result_value: ValidResult = {
                "result": True,
                "text": text[0:st],
                "size": st,
                "obj": obj
            }
            return result_value
        st += res["size"]

        # expression multiplicative

        res_mul = self.isValid(text[st:])
        if res_mul == False:
            return False
        st += res_mul["size"]

        obj = MathMultiplicative(res_pow["obj"], res["text"], res_mul["obj"])
        result_value: ValidResult = {
            "result": True,
            "text": text[0:st],
            "size": st,
            "obj": obj
        }
        return result_value
    