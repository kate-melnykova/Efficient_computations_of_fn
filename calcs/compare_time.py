import timeit
import math
from decimal import Decimal


def get_time_consumption(foo, n_runs=1000):
    """
    compute mean and std of runtime of foo over n_runs runs
    :param foo: function whose runtime is measured
    :param n_runs: total number of runs
    :return: mean and std of runtime as a tuple
    """
    timer = timeit.Timer(foo, number=1)
    sum_ = Decimal(0)
    sum_squares = Decimal(0)
    for _ in range(n_runs):
        elapsed = Decimal(timer.timeit(number=1))
        sum_ += elapsed
        sum_squares += elapsed * elapsed
    std = math.sqrt((sum_squares - sum_ * sum_)/Decimal(n_runs))
    mean = sum_ / Decimal(n_runs)
    return mean, std


def refine_estimates(foo, mean: Decimal, std: Decimal, n_runs, add_m_runs):
    """
    add additional runs to estimation
    :param foo:
    :param mean:
    :param std:
    :param n_runs:
    :param add_m_runs:
    :return:
    """
    sum_ = mean * n_runs
    std *= std
    sum_squares = std * n_runs + sum_ * sum_


