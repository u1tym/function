
# 正規表現を使うためのモジュール
import re

class Tokens:

    def __init__(self):
        self.patterns = []

        self.last_proc_string = ""
        self.last_proc_position = -1
        self.last_error_message = ""
        return

    def add(self, add_pattern):
        self.patterns.append(add_pattern)
        return

    def last_error(self):
        print(self.last_error_message)
        print(self.last_proc_string)
        for cnt in range(self.last_proc_position):
            print(" ", end="")
        print("^")
        return

    def analyze(self, function_string):
        target_string = function_string.replace(" ", "")

        # どこを処理中かを表す情報
        self.last_error_message = ""

        proc_string = target_string
        proc_position = 0

        result = []
        while len(target_string) > 0:
            match = None
            for pattern in self.patterns:
                match = re.match(pattern, target_string)
                if match is None:
                    continue
                break

            if match is None:
                self.last_proc_string = proc_string
                self.last_proc_position = proc_position
                self.last_error_message = "analyze_error"
                return None

            result.append(match.group(0))
            target_string = target_string[match.end(0):]

            # 処理位置をずらす
            proc_position += match.end(0)

        return result


def main():

    token = Tokens()
    token.add(r'(0|[1-9][0-9]*)')
    token.add(r'(\+|-|\*|/)')

    result = token.analyze("3 * 11 + x + 1")
    if result is None:
        token.last_error()
    else:
        print(result)


if __name__ == '__main__':

    main()


