from typing import Dict
from time import time


def factorial(uuid: str, results: dict, parameter_names: list):
    """
    :param uuid: unique identifier of the string
    :param results: global variable that keeps track of the progress
    :param parameter_names: verifies all args' names that are passed to function
    :return: the value of n!

    The algorithm is given at
    https://pdfs.semanticscholar.org/7388/ef8a3fa31b2d01f2835b3beeccdb16c0616a.pdf
    """
    assert set(parameter_names) == set(['argument', 'time_limit', 'accuracy'])

    n = int(results[uuid]['argument'])
    time_limit = float(results[uuid]['time_limit'])
    accuracy = int(results[uuid]['accuracy'])
    max_time = time() + time_limit

    if n < 8:
        print([1, 2, 6, 24, 120, 720, 5040][n-1])
        factorial_val = [1, 2, 6, 24, 120, 720, 5040][n-1]
        enough_time = True
        results[uuid]['status'] = 'COMPLETED'
    else:

        if n % 2 == 0:
            factorial_val = 1
        else:
            # reduce to even number
            factorial_val = n
            n = n - 1

        list_integ = list(range(2, n+1, 2))
        enough_time = True
        sums = [sum(list_integ[i:]) for i in range(int(n/2))]

        assert len(list_integ) == int(n/2)

        for i in range(int(n/2)):
            if time() > max_time:
                enough_time = False
                break
            factorial_val *= sums[i]

        results[uuid]['status'] = 'COMPLETED'

    # store results depending if there is enough time
    if enough_time:
        results[uuid]['enough_time?'] = 'yes'

        # update factorial_val to keep accuracy-many digits
        factorial_val = str(factorial_val)
        if len(str(factorial_val)) > accuracy:
            factorial_val = factorial_val[:accuracy] + "E+" + str(len(factorial_val) - accuracy)

        results[uuid]['value'] = factorial_val
    else:
        results[uuid]['enough_time?'] = 'no'
        results[uuid]['value'] = None


if __name__ == '__main__':
    uuid = '1'
    results = {'1': dict()}
    results[uuid]['argument'] = int(input('Enter the argument: '))
    results[uuid]['time_limit'] = 3
    results[uuid]['accuracy'] = int(input('Enter the accuracy (number of digits displayed): '))
    factorial(uuid, results, ['argument', 'time_limit', 'accuracy'])
    print(results)



