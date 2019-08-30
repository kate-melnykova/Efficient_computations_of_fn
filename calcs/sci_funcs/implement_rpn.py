from typing import List
from decimal import Decimal
import numpy as np
from operator import add, sub, mul, truediv, pow

from convert_to_rpn import functions, names

convert_alg_to_func = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow
}


def compute_rpn(s: List[Decimal or str]) -> Decimal:
    temp_stack = []
    while s:
        elem = s.pop(0)
        if isinstance(elem, Decimal):
            temp_stack.append(elem)
        else:
            if elem in ['+', '-', '*', '/', '^']:
                operator = convert_alg_to_func[elem]
                # implement action on last two elements of temp_stack
                term2 = temp_stack.pop()
                term1 = temp_stack.pop()
                temp_stack.append(operator(term1, term2))
            else:
                [operator, nargs] = functions[elem]
                terms = temp_stack[-nargs:]
                terms = [float(term) for term in terms]
                temp_stack = temp_stack[:-nargs]
                temp_stack.append(operator(*terms))

    if len(temp_stack) != 1:
        raise
    return temp_stack[0]
