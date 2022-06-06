数式解析クラス

ex)
import function

f = function.function("x^2 + x - 1")
f.print()

v = f.getValue("x", 1)

g = f.diff("x")
g.print()

