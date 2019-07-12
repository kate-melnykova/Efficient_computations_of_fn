from time import time
def factorial(n: int, time_limit=10)->int:
    """
    :param n:
    :return: the value of n!
    The algorithm is given at
    https://pdfs.semanticscholar.org/7388/ef8a3fa31b2d01f2835b3beeccdb16c0616a.pdf
    """
    n = int(n)
    time_limit = 10
    max_time = time() + time_limit
    error = None
    if n < 7:
        print([1, 2, 6, 24, 120, 720, 5040][n-1])
        factorial_val = [1, 2, 6, 24, 120, 720, 5040][n-1]
        return [factorial_val, len(str(factorial_val))]
    if n%2 == 0:
        factorial_val = 1
    else:
        factorial_val = n
        n = n - 1 # reduce to even number

    list_integ = list(range(0,n+1,2))
    acc = 1
    sums = [sum(list_integ[i:]) for i in range(int(n/2))]
    for i in range(int(n/2)):
        if time() > max_time:
            acc = 0
            break
        factorial_val *= sums[i]
    #print(factorial_val)
    if acc:
        acc = len(str(factorial_val))
    print(factorial_val)
    print(acc)
    return [factorial_val, acc]

if __name__ == '__main__':
    factorial(input("Enter the integer: "))



