from typing import *
from profitable import get_profitable
import random
random.seed()


def greed_search(keys: List[str]):
    border_std = 3
    max_mean = 0
    real_std = 0
    res_package = (0, 0, 0, 0, 0)

    for i in range(100):
        packege = _get_random_package(len(keys))
        params = _get_params_for_package(packege, keys)

        if params[0] < border_std and params[1] > max_mean:
            max_mean = params[1]
            real_std = params[0]
            res_package = packege

    return res_package, max_mean, real_std


def _get_params_for_package(package: List[float], keys: List[str]):
    data = _get_data(keys)
    s_mean = 0
    s_std = 0
    i = 0
    for key in keys:
        s_mean += data[key][0]*package[i]
        s_std += data[key][1]*package[i]

        i += 1

    return s_std, s_mean


def _get_random_package(count: int):
    border = 10000
    res = []
    for i in range(count-1):
        current_value = random.randint(0, border)
        res.append(current_value/10000)
        border -= current_value
    res.append(border/10000)

    return res


def _get_data(keys: List[str]):
    res = {}
    for key in keys:
        res[key] = get_profitable(key)

    return res

