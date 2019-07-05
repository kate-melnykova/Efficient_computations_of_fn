from decimal import Decimal
from decimal import getcontext
from time import time
def compute_pi(time_limit=10,n_digits=1000)->float:
    """
    The implementation of the Chudnovsky algorithm
    https://en.wikipedia.org/wiki/Chudnovsky_algorithm
    :param n_digits:
    :return:
    """
    n_digits = int(n_digits)
    max_time = time() + int(time_limit)
    #initialize
    getcontext().prec = n_digits + 3
    C = 426880 * Decimal(10005).sqrt()
    L = 13591409
    X = 1
    M = 1
    K = 6
    M = 1
    idx = 1

    Sum = Decimal(M * L) / X

    #run
    while time() < max_time:
        M *= (K**3 - 16*K) // (idx + 1)**3
        K += 12
        idx += 1

        L += 545140134
        X *= -262537412640768000
        term = Decimal(M * L) / X
        Sum += term

        #print(str(term)[2:n_digits+3])
        if round(term, n_digits+5) == 0:
            break

    pi_val = C / Sum
    pi_val = str(pi_val)[:n_digits+2]
    term = str(term)
    #accuracy = str(term).lstrip('-')
    accuracy = int(term[term.index('E')+2:])
    print("Pi(time={}, disp={} digits) = \n {}".format(time_limit, n_digits, pi_val))

    return Decimal(pi_val)#, accuracy


if __name__ == '__main__':
    time_limit = input("Time limit in sec: ")
    n_digits = input("Number of digits: ")
    compute_pi(time_limit, n_digits)