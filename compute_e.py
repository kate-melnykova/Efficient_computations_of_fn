from collections import defaultdict
from time import time
from decimal import Decimal
from decimal import getcontext


def compute_e(uuid: str, results: dict, parameter_names: list):
    """
    :param uuid: unique identifier of the string
    :param results: global variable that keeps track of the progress
    :param parameter_names: verifies all args' names that are passed to function

    This function computes the Euler number e
    within given time_limit and displays
    n_digits of it

    Here I use Brothers' Formulae
    https://www.intmath.com/exponential-logarithmic-functions/calculating-e.php
    """
    assert set(parameter_names) == set(['time_limit', 'accuracy'])

    time_limit = float(results[uuid]['time_limit'])
    accuracy = int(results[uuid]['accuracy'])
    max_time = time() + time_limit

    # initialize
    getcontext().prec = accuracy + 3
    e_val = Decimal('0')
    two_n_plus_two = Decimal('2')
    two_n_plus_one_fact_inv = Decimal('1')
    accuracy_achieved = 0
    enough_time = 'yes'

    # run
    while accuracy_achieved >= accuracy:
        if time() < max_time:
            term = two_n_plus_two * two_n_plus_one_fact_inv
            e_val += term
            two_n_plus_one_fact_inv /= (two_n_plus_two * (two_n_plus_two + 1))
            two_n_plus_two += 2
            if two_n_plus_one_fact_inv == 0:
                break

            term = str(term)
            accuracy_achieved = int(term[term.index('E') + 2:])
        else:
            enough_time = 'no'
            break

    # save only true digits of e_val
    e_val = round(e_val, accuracy_achieved)

    # save results
    results[uuid]['status'] = 'COMPLETED'
    results[uuid]['value'] = e_val
    results[uuid]['enough_time'] = enough_time
    results[uuid]['accuracy_achieved'] = accuracy_achieved


if __name__ == '__main__':
    uuid = '1'
    results = {'1': dict()}
    results[uuid]['time_limit'] = 3
    results[uuid]['accuracy'] = int(input('Enter the accuracy (number of digits displayed): '))
    factorial(uuid, results, ['time_limit', 'accuracy'])
    print(results)




