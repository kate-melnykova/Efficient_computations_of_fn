from collections import defaultdict
from decimal import Decimal
from decimal import getcontext
from time import time


def compute_pi(time_limit, accuracy, uuid, results):
    """
    The implementation of the Chudnovsky algorithm
    https://en.wikipedia.org/wiki/Chudnovsky_algorithm
    :param accuracy:
    :return:
    """
    accuracy = int(accuracy)
    max_time = time() + float(time_limit)
    getcontext().prec = accuracy + 300
    print(getcontext())

    # initialize
    c = Decimal('426880') * Decimal('10005').sqrt()
    l = Decimal('13591409')
    x = Decimal('1')
    m = Decimal('1')
    k = Decimal('6')
    idx = 1

    sum_ = m * l / x

    #run
    while time() < max_time:
        m *= (k**3 - 16*k) // (idx + 1)**3
        k += 12
        idx += 1

        l += Decimal('545140134')
        x *= Decimal('-262537412640768000')
        term = round(m * l / x, accuracy + 3)
        sum_ += term
        # print(term)
        if term == 0:
            break

    pi_val = c / sum_
    pi_val = str(pi_val)[:accuracy+2]
    term = str(term)
    accuracy_achieved = int(term[term.index('E')+2:])

    print(pi_val)
    print(accuracy_achieved)
    results[uuid]['result'] = 'COMPLETED'
    results[uuid]['value'] = pi_val
    results[uuid]['accuracy_achieved'] = accuracy_achieved


if __name__ == '__main__':
    time_limit = input("Time limit in sec: ")
    accuracy = input("Number of digits: ")
    compute_pi(time_limit, accuracy, "", defaultdict(dict))