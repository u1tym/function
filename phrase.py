import re
import pandas as pd

from typing import Any
from typing import TypedDict
from typing import NamedTuple
from typing import Optional
from typing import Self


class CsvRec(NamedTuple):
    """CSVファイルのレコード定義"""
    name: str
    expression: str
    priority: int

class RegRec(TypedDict):
    """内部保持形式"""
    nm: str
    ex: str
    rg: re.Pattern

class AnalyzeResult(TypedDict):
    """解析結果"""
    name: str
    value: str
    next: int


class Phrese:
    """
    語句を解析するためのクラス
    """

    def __init__(self: Self, filename: Optional[str] = None) -> None:
        """コンストラクタ"""

        # 内部保持テーブルを初期化
        self._regs: list[RegRec] = []

        # ファイル名指定時は読み込み
        if filename is not None:
            self.read(filename)

        return
    
    def debug(self: Self) -> None:
        for r in self._regs:
            print(r["nm"], r["ex"])

    def read(self: Self, filename: str) -> None:
        try:
            df = pd.read_csv(filename, skipinitialspace=True, quotechar="'")

            rec: Any
            for rec in df.itertuples(index=False, name="CsvRec"):
                phrase_rec = CsvRec(*rec)

                nm: str = phrase_rec.name
                ex: str = phrase_rec.expression

                self.add(nm, ex)

        except Exception as ex:
            print("読み込み処理異常 " + filename + " " + str(ex))
            pass

        return

    def add(self: Self, name: str, expr: str) -> None:
        names: list[str] = [d["nm"] for d in self._regs]
        if name in names:
            return
        
        # コンパイル
        rg: re.Pattern = re.compile(expr)

        # 追加
        self._regs.append({
            "nm": name,
            "ex": expr,
            "rg": rg
        })


    def analyze(self: Self, f: str) -> Optional[AnalyzeResult]:
        idx: int = 0
        while True:
            if idx >= len(f):
                return None
            
            if f[idx] != " ":
                break
            idx += 1
        
        for rec in self._regs:
            p: re.Pattern = rec["rg"]

            matchObj: Optional[re.Match] = p.match(f[idx:])
            if matchObj is not None:
                return {
                    "name": rec["nm"],
                    "value": matchObj.group(),
                    "next": matchObj.end()
                }

        return None
