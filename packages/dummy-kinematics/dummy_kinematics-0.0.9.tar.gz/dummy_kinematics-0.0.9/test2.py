from decimal import Decimal
from typing import Iterable, Tuple


def index_number(li: Iterable, target: float) -> Tuple[int, float]:
    """返回从序列中找最接近给定值的数值及索引，返回（索引，目标值）

    :param _type_ li: 目标序列
    :param _type_ target: 目标值
    :return Tuple[int,float]: （索引，结果值）

    """

    select = Decimal(str(target)) - Decimal(str(li[0]))
    index = 0
    for i in range(1, len(li) - 1):
        select2 = Decimal(str(target)) - Decimal(str(li[i]))
        if (abs(select) > abs(select2)):
            select = select2
            index = i
    return index, li[index]


def index2(li: Iterable, target: float) -> Tuple[int, float]:
    res = min(enumerate(li), key=lambda tup: abs(tup[1] - target))
    return res


a = [1, 2, 3, 4.4, 5.4]
print(index_number(a, 4.5))
print(index2(a, 4.5))
