
# 正規表現を使うためのモジュール
import re

def main():

    # Goal
    # 文字列を分解すること
    #
    # str1 = "3 * 11 + 1"
    # ↓
    # div_str1 = ["3", "*", "11", "+", "1"]

    # 正規表現を使った文字列の適合解析
    # 整数
    ptn_number = r'(0|[1-9][0-9]*)'
    # 演算子
    ptn_operator = r'(\+|-|\*|/)'

    compiled_ptn_number = re.compile(ptn_number)
    compiled_ptn_operator = re.compile(ptn_operator)

    test_string = "123"
    match_1 = compiled_ptn_number.match(test_string)
    match_2 = compiled_ptn_operator.match(test_string)
    print(match_1) # 123
    print(match_2) # None

    test_string = "00"
    match_1 = compiled_ptn_number.match(test_string)
    match_2 = compiled_ptn_operator.match(test_string)
    print(match_1) # 0 (00ではない)
    print(match_2) # None

    test_string = "+*"
    match_1 = compiled_ptn_number.match(test_string)
    match_2 = compiled_ptn_operator.match(test_string)
    print(match_1) # None
    print(match_2) # + (+だけ)

    # match_n : マッチオブジェクト
    #   match_n.group(0) マッチした文字列
    #   match_n.end(0)   マッチした文字列長
    #   グループにカラム機能を使っていないので、添え字は0のみ

    # cf)
    # import re
    # mobj = re.match(r'([0-9]*) ([0-9]*)', '1 2 33 4')
    # mobj.group(0)  # 1 2
    # mobj.group(1)  # 1
    # mobj.group(2)  # 2
    # ()で囲まれた部分がグループになって、その部分だけアクセスできる
    # ようになる。


if __name__ == '__main__':

    main()


