from expression import Expression
from expression import ValidResult

from phrase import Phrese
from expression_multiplicative import ExpressionMultiplicative
from math_additive import MathAdditive

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class ExpressionAdditive(Expression):
    phrase: str = "phrase_mathmatics.csv"

    def __init__(self: Self) -> None:
        self._mul = ExpressionMultiplicative(self.phrase)
        self._phr = Phrese(self.phrase)

    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:

        st: int = 0

        # express multiplicative
        res_mul = self._mul.isValid(text[st:])
        if res_mul == False:
            return False
        st += res_mul["size"]

        # +-
        res = self._phr.analyze(text[st:])
        if res is None:
            obj = MathAdditive(res_mul["obj"])
            result_value: ValidResult = {
                "result": True,
                "text": text[0:st],
                "size": st,
                "obj": obj
            }
            return result_value
        st += res["size"]

        # express additive
        res_add = self.isValid(text[st:])
        if res_add["result"] == False:
            return False
        st += res_add["size"]

        obj = MathAdditive(res_mul["obj"], res["text"], res_add["obj"])
        result_value: ValidResult = {
            "result": True,
            "text": text[0:st],
            "size": st,
            "obj": obj
        }
        return result_value
    