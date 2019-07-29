from collections import defaultdict
from decimal import Decimal
from decimal import getcontext
from time import time


def compute_pi(arguments: dict, parameter_names: list):
    """
    :param uuid: unique identifier of the string
    :param results: global variable that keeps track of the progress
    :param parameter_names: verifies all args' names that are passed to function

    The implementation of the Chudnovsky algorithm
    https://en.wikipedia.org/wiki/Chudnovsky_algorithm
    :param accuracy:
    :return:
    """
    assert set(parameter_names) == set(['time_limit', 'accuracy'])

    time_limit = float(arguments['time_limit'])
    accuracy = int(arguments['accuracy'])
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

    # run
    max_time = time() + time_limit
    while time() < max_time:
        m *= (k**3 - 16*k) // (idx + 1)**3
        k += 12
        idx += 1

        l += Decimal('545140134')
        x *= Decimal('-262537412640768000')
        term = round(m * l / x, accuracy + 3)
        sum_ += term
        if term == 0:
            enough_time = 'yes'
            break

    pi_val = c / sum_

    term = str(term)
    if enough_time:
        accuracy_achieved = accuracy
    else:
        if 'E' in term:
            accuracy_achieved = int(term[term.index('E') + 2:])
        else:
            accuracy_achieved = len(term) - len(term.lstrip('0'))

    # save only true digits of e_val
    pi_val = round(pi_val, accuracy_achieved)

    # save results
    arguments['status'] = 'COMPLETED'
    arguments['value'] = pi_val
    arguments['enough_time'] = enough_time
    arguments['accuracy_achieved'] = accuracy_achieved