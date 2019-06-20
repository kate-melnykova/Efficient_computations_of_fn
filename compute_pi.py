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
    start_time = time()
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
    while time() < start_time + float(time_limit):
        M *= (K**3 - 16*K) // (idx + 1)**3
        K += 12
        idx += 1

        L += 545140134
        X *= -262537412640768000

        Sum += Decimal(M * L) / X

    pi_val = C / Sum
    pi_val = str(pi_val)[:n_digits]
    print("Pi(time={}, disp={} digits) = \n {}".format(time_limit, n_digits, pi_val))
    return Decimal(pi_val)


if __name__ == '__main__':
    time_limit = input("Time limit in sec: ")
    compute_pi(time_limit)