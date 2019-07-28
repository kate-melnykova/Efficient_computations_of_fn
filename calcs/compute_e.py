from collections import defaultdict
from time import time
from decimal import Decimal
from decimal import getcontext


def compute_e(arguments: dict, parameter_names: list):
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

    time_limit = float(arguments['time_limit'])
    accuracy = int(arguments['accuracy'])
    max_time = time() + time_limit

    # initialize
    getcontext().prec = accuracy + 3
    e_val = Decimal('0')
    two_n_plus_two = Decimal('2')
    two_n_plus_one_fact_inv = Decimal('1')
    term = two_n_plus_two * two_n_plus_one_fact_inv
    accuracy_achieved = accuracy
    enough_time = 'yes'

    # run
    while term != 0:
        if time() < max_time:
            term = two_n_plus_two * two_n_plus_one_fact_inv
            e_val += term
            two_n_plus_one_fact_inv /= (two_n_plus_two * (two_n_plus_two + 1))
            two_n_plus_two += 2
            if two_n_plus_one_fact_inv == 0:
                break

            term = str(term)
        else:
            enough_time = 'no'
            if 'E' in term:
                accuracy_achieved = int(term[term.index('E') + 2:])
            else:
                accuracy_achieved = len(term) - len(term.lstrip('0'))
            break

    # save only true digits of e_val
    e_val = round(e_val, accuracy_achieved)

    # save results
    arguments['status'] = 'COMPLETED'
    arguments['value'] = e_val
    arguments['enough_time'] = enough_time
    arguments['accuracy_achieved'] = accuracy_achieved




