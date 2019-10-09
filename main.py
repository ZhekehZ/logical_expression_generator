#!/usr/bin/python3

import pandas as pd
import sys
from generate_from_table import generate_dnf


def displayConj(implicands):
    res = []
    for impl in implicands:
        impl_list = [('~x' if impl[i] < 0 else 'x') + str(i + 1) for i in range(len(impl)) if impl[i]]
        res.append(' & '.join(impl_list))
    print(' | '.join(res))


def option1(argv):
    table = pd.read_csv(argv)
    col_names = ['x' + str(i) for i in range(1, len(table.columns))] + ['y']
    table.columns = col_names
    table = table[table.y == 1].drop(['y'], axis=1)
    table = table.apply(lambda x: x * 2 - 1)
    
    implic, others = generate_dnf(table)
    
    displayConj(implic)
    for i in others:
        implic.append(i)
        displayConj(implic)


def main(argv):
    if len(argv) != 2:
        msg = """error:
    Invalid arguments.
    Usage:  ./main.py table.csv
        """
        print(msg)
    else:
        option1(argv[1])


if __name__ == '__main__':
    main(sys.argv)
