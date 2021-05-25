from typing import *
from profitable import get_profitable
import random
random.seed()


def greed_search(keys: List[str], border_std=0.03, size_iterations=1000):
    max_mean = 0
    real_std = 0
    res_package = (0, 0, 0, 0, 0)

    for i in range(size_iterations):
        packege = _get_random_package(len(keys))
        params = _get_params_for_package(packege, keys)

        if params[0] < border_std and params[1] > max_mean:
            max_mean = params[1]
            real_std = params[0]
            res_package = packege

    return {"package": res_package, "mean": max_mean, "std": real_std}


def gradient_search(keys: List[str], border_std=0.03, start_step_border=0.3, size_iterations=1000):
    max_mean = 0
    real_std = 0
    res_package = (0, 0, 0, 0, 0)
    step_border = start_step_border

    for i in range(size_iterations):
        packege = _make_step(res_package, step_border)
        step_border -= start_step_border / size_iterations

        params = _get_params_for_package(packege, keys)
        if params[0] < border_std and params[1] > max_mean:
            max_mean = params[1]
            real_std = params[0]
            res_package = packege

    return {"package": res_package, "mean": max_mean, "std": real_std}


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


def _make_step(last_package: List[float], step_border: float):
    stepped_packeges = []
    for factor in last_package:
        current_step = random.randint(0, round(step_border * 1000))/1000 - step_border / 2
        new_factor = factor + current_step
        if new_factor < 0:
            new_factor = -1 * new_factor / 2

        stepped_packeges.append(factor + new_factor)

    normalize_package = _normalize_package(stepped_packeges)

    return normalize_package


def _normalize_package(package: List[float]):
    sum_value = sum(package)
    normalize_factor = 1 / sum_value

    return [faction * normalize_factor for faction in package]


def _get_data(keys: List[str]):
    res = {}
    for key in keys:
        res[key] = get_profitable(key)

    return res

