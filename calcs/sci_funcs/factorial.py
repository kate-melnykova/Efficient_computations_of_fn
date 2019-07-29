from typing import Dict
from time import time


def factorial(arguments: dict, parameter_names: list):
    """
    :param uuid: unique identifier of the string
    :param results: global variable that keeps track of the progress
    :param parameter_names: verifies all args' names that are passed to function

    The algorithm is given at
    https://pdfs.semanticscholar.org/7388/ef8a3fa31b2d01f2835b3beeccdb16c0616a.pdf
    """
    assert set(parameter_names) == set(['argument', 'time_limit', 'accuracy'])
    n = int(arguments['argument'])
    time_limit = float(arguments['time_limit'])
    accuracy = int(arguments['accuracy'])
    max_time = time() + time_limit

    if n < 8:
        print([1, 2, 6, 24, 120, 720, 5040][n-1])
        factorial_val = [1, 2, 6, 24, 120, 720, 5040][n-1]
        enough_time = True
        arguments['status'] = 'COMPLETED'
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

        arguments['status'] = 'COMPLETED'

    # store results depending if there is enough time
    if enough_time:
        arguments['enough_time'] = 'yes'

        # update factorial_val to keep accuracy-many digits
        factorial_val = str(factorial_val)
        if len(str(factorial_val)) > accuracy:
            factorial_val = factorial_val[:accuracy] + "E+" + str(len(factorial_val) - accuracy)

        arguments['value'] = factorial_val
    else:
        arguments['enough_time'] = 'no'
        arguments['value'] = None



