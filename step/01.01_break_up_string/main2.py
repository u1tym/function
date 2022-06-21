
# 正規表現を使うためのモジュール
import re

def main():

    # Goal
    # 文字列を分解すること
    #
    # str1 = "3 * 11 + 1"
    # ↓
    # div_str1 = ["3", "*", "11", "+", "1"]

    str1 = "3 * 11 + 1"
    result = analyze(str1)
    print(result)


def analyze(function_string):

    # 空白除去
    target_string = function_string.replace(" ", "")

    # 正規表現パターンを定義
    tokens = [ r'(0|[1-9][0-9]*)',      # 整数
               r'(\+|-|\*|/)' ]         # 演算子

    # 結果用の器
    result = []

    while len(target_string) > 0:

        # 一致する正規表現を探す
        match = None
        for token in tokens:
            match = re.match(token, target_string)
            if match is None:
                continue
            break

        # 一致するものが無いときは、処理できない
        if match is None:
            return []

        # 一致したものを「結果」に追加して、続ける
        result.append(match.group(0))
        target_string = target_string[match.end(0):]

    return result


if __name__ == '__main__':

    main()


