from expression import Expression
from expression import ValidResult

from expression_additive import ExpressionAdditive
from math_formula import MathFormula

from typing import TypedDict
from typing import Union
from typing import Literal
from typing import Any
from typing import Self

class Expressionformula(Expression):
    phrase: str = "phrase_mathmatics.csv"

    def __init__(self: Self) -> None:
        self._add = ExpressionAdditive(self.phrase)

    def isValid(self: Self, text: str) -> Union[Literal[False], ValidResult]:

        # expression-additive
        res = self._add.isValid(text)
        if res == False:
            return False
        
        obj = MathFormula(res["obj"])
        
        result_value: ValidResult = {
            "result": True,
            "text": res["text"],
            "size": res["size"],
            "obj": obj
        }
        return result_value
    