from decimal import Decimal
from decimal import getcontext
from time import time
from typing import List, Dict


def compute_pi(accuracy: int) -> Decimal:
    """
    :param arguments: contains all input data for the computation
    :param parameter_names: name of parameters

    Computes pi within given time_limit and keeps
    accuracy-many of it. If there is not enough time, only
    accuracy_achieved-many digits are displayed

    Computation uses the Chudnovsky algorithm
    https://en.wikipedia.org/wiki/Chudnovsky_algorithm
    """

    getcontext().prec = accuracy + 300

    # initialize
    c = Decimal('426880') * Decimal('10005').sqrt()
    l = Decimal('13591409')
    x = Decimal('1')
    m = Decimal('1')
    k = Decimal('6')
    idx = 1
    enough_time = 'no'
    sum_ = m * l / x
    term = 1 # fake value to start the loop
    while term != 0:
        m *= (k**3 - 16*k) // (idx + 1)**3
        k += 12
        idx += 1

        l += Decimal('545140134')
        x *= Decimal('-262537412640768000')
        term = round(m * l / x, accuracy + 3)
        sum_ += term

    pi_val = c / sum_

    # return only digits of pi_val requested
    return round(pi_val, accuracy)