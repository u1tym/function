# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

import re


def main():
    ex: str = "(0|[-]*[1-9][0-9]*)"
    rg: re.Pattern = re.compile(ex)

    f: str = "5 + 3 / 2"
    matchObj = rg.match(f)
    if matchObj is None:
        print("None")
    else:
        print(matchObj.group())
    return

if __name__ == '__main__':
    main()
