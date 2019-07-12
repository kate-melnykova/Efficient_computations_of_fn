from time import time
from decimal import Decimal
from decimal import getcontext
def compute_e(time_limit=10, n_digits=1000):
    """
    This function computes the Euler number e
    within given time_limit and displays
    n_digits of it

    Here I use Brothers' Formulae
    https://www.intmath.com/exponential-logarithmic-functions/calculating-e.php
    :param time_limit:
    :param n_digits:
    :return: value of e
    """
    n_digits = int(n_digits)
    start_time = time()
    # initialize
    getcontext().prec = n_digits + 5
    e_val = 0
    two_n_plus_two = 2
    two_n_plus_one_fact_inv = Decimal(1)

    accuracy = 0
    #run
    while time() < start_time + time_limit or accuracy >= n_digits:
        term = two_n_plus_two * two_n_plus_one_fact_inv
        e_val += term
        two_n_plus_one_fact_inv /= (two_n_plus_two * (two_n_plus_two + 1))
        two_n_plus_two += 2
        if two_n_plus_one_fact_inv == 0:
            break
    term = str(term)
    accuracy = int(term[term.index('E') + 2:])

    return [e_val, accuracy]

if __name__ == '__main__':
    n_digits = input("Enter the number of digits of interest")
    compute_e(3, n_digits)




