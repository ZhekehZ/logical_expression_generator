"""
    Построение ДНФ методом Куайна
    https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%9A%D1%83%D0%B0%D0%B9%D0%BD%D0%B0
"""

import pandas as pd


def list_to_int(lst):
    """
        [-1,0,1,-1] == ~x1 & x3 & ~x4 --> int
    """
    pow3 = 1
    acc = 0
    for i in lst:
        acc += (i + 1) * pow3
        pow3 *= 3
    return acc


def int_to_iist(num, length):
    """
        length -- количество переменных
    """
    res = []
    for _ in range(length):
        res.append(num % 3 - 1)
        num //= 3
    return res


def unite(expr1, expr2):
    """
        Объединение двух дизъюнктов
    """
    neg = 0
    pos_neg = 0
    for i, val in enumerate(expr1):
        if val == expr2[i]:
            continue
        elif val == -expr2[i]:
            neg += 1
            pos_neg = i
        else:
            return None
    if neg != 1:
        return None
    expr = expr1.copy()
    expr[pos_neg] = 0
    return expr


def is_subexpr(expr1, expr2):
    for i, val in enumerate(expr1):
        if val == 0:
            continue
        elif val != expr2[i]:
            return False
    return True


def create_preconj(table):
    """
        Получение сокращённой формы
    """
    var = set()
    length = table.shape[1]
    for _, row in table.iterrows():
        var.add(list_to_int(list(row)))

    results = set()
    while True:
        next_iter_set = set()
        already = set()
        for i, el1 in enumerate(var):
            count = 0
            for j, el2 in enumerate(var):
                if j <= i:
                    continue
                arg1 = int_to_iist(el1, length)
                arg2 = int_to_iist(el2, length)
                new_elem = unite(arg1, arg2)
                if new_elem:
                    next_iter_set.add(list_to_int(new_elem))
                    count += 1
                    already.add(j)
                    already.add(i)
            if i not in already:
                results.add(el1)
        if not next_iter_set:
            break
        else:
            var = next_iter_set
    return results


def filter_preconjs(prec, table):
    """
        Получение минимальной формы
    """
    prec = list(prec)
    implic_table = []
    length = table.shape[1]
    for conj in prec:
        t_row = []
        for _, row in table.iterrows():
            t_row.append(is_subexpr(int_to_iist(conj, length), list(row)))
        implic_table.append(t_row)
    implic_table = pd.DataFrame(implic_table)

    implicands = set()
    not_covered_columns = set(range(implic_table.shape[1]))
    for col in implic_table:
        if sum(implic_table[col]) == 1:
            idx = implic_table.index[implic_table[col]]
            implicands.add(prec[idx[0]])
            row = implic_table.iloc[idx[0]]
            cols = [i for i in range(len(row)) if row[i]]
            not_covered_columns -= set(cols)

    if not_covered_columns:
        table1 = implic_table[list(not_covered_columns)]
        counts = []
        for i, row in table1.iterrows():
            counts.append([i, sum(list(row))])
        counts.sort(key=lambda x: -x[1])
        while not_covered_columns:
            idx = counts[0][0]
            implicands.add(prec[idx])
            row = implic_table.iloc[idx]
            cols = [i for i in range(len(row)) if row[i]]
            not_covered_columns -= set(cols)

    others = set(prec) - implicands
    return implicands, others


def generate_dnf(table):
    step1 = create_preconj(table)
    implic, others = filter_preconjs(step1, table)
    implic = list(map(lambda x: int_to_iist(x, table.shape[1]), implic))
    others = list(map(lambda x: int_to_iist(x, table.shape[1]), others))
    return implic, others
