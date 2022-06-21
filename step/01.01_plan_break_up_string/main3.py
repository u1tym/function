
# 正規表現を使うためのモジュール
import re

class Tokens:

    def __init__(self):
        self.patterns = []
        return

    def add(self, add_pattern):
        self.patterns.append(add_pattern)
        return

    def analyze(self, function_string):
        target_string = function_string.replace(" ", "")

        result = []
        while len(target_string) > 0:
            match = None
            for pattern in self.patterns:
                match = re.match(pattern, target_string)
                if match is None:
                    continue
                break
            if match is None:
                return []

            result.append(match.group(0))
            target_string = target_string[match.end(0):]

        return result


def main():

    token = Tokens()
    token.add(r'(0|[1-9][0-9]*)')
    token.add(r'(\+|-|\*|/)')

    result = token.analyze("3 * 11 + 1")
    print(result)

if __name__ == '__main__':

    main()


