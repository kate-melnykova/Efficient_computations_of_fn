from collections import defaultdict
from time import time
from decimal import Decimal
from decimal import getcontext


def compute_e(time_limit, accuracy, uuid, results):
    """
    This function computes the Euler number e
    within given time_limit and displays
    n_digits of it

    Here I use Brothers' Formulae
    https://www.intmath.com/exponential-logarithmic-functions/calculating-e.php
    :param time_limit: time limit
    :param accuracy: number of digits requested
    :param uuid: unique identifier of computation
    :param results: global file for tracking the progress
    """
    time_limit = float(time_limit)
    accuracy = int(accuracy)

    start_time = time()
    # initialize
    getcontext().prec = accuracy + 3
    e_val = Decimal('0')
    two_n_plus_two = Decimal('2')
    two_n_plus_one_fact_inv = Decimal('1')

    accuracy_achieved = 0
    # run
    while time() < start_time + time_limit or accuracy_achieved >= accuracy:
        term = two_n_plus_two * two_n_plus_one_fact_inv
        e_val += term
        two_n_plus_one_fact_inv /= (two_n_plus_two * (two_n_plus_two + 1))
        two_n_plus_two += 2
        if two_n_plus_one_fact_inv == 0:
            break

    term = str(term)
    accuracy_achieved = int(term[term.index('E') + 2:])

    # save results

    results[uuid]['result'] = 'COMPLETED'
    results[uuid]['value'] = e_val
    results[uuid]['accuracy_achieved'] = accuracy_achieved


if __name__ == '__main__':
    accuracy = input("Enter the number of digits of interest")
    compute_e(3, accuracy, "", defaultdict(dict))




