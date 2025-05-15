# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

from phrase import Phrese

import json

def main() -> None:
    a = Phrese("phrase_mathmatics.csv")
    a.debug()

    res = a.analyze("5 + 3 / 2")
    print(json.dumps(res, indent=4))

    return


if __name__ == '__main__':
    main()

