from typing import *
import yfinance as yf
from pandas import DataFrame
from numpy import mean, std
import json
import random
random.seed()


def get_profitable(key: str):
    with open('./profitable-cach.json', 'r') as file:
        cached_profitable = json.load(file)

    if key not in cached_profitable.keys():
        return _write_to_catch(key)

    return cached_profitable[key]


def _write_to_catch(key: str):
    s, m = _request_profitable(key)
    cached_profitable = {}
    with open('profitable-cach.json', 'r') as file:
        cached_profitable = json.load(file)

    with open('profitable-cach.json', 'w') as file:
        cached_profitable[key] = [s, m]
        json.dump(cached_profitable, file)

    return s, m


def _request_profitable(key: str):
    df_order: DataFrame = yf.download(key, '2010-11-01', '2021-05-01')['Adj Close']
    profit_sum = 0
    profitability: List[float] = []

    last_order = df_order[0]
    for order in df_order[1:]:
        profit = order - last_order
        profitability.append(profit)
        profit_sum += profit
        last_order = order

    return std(profitability), mean(profitability)
