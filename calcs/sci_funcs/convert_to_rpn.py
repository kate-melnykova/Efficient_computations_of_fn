"""
convert infix notation to rpn
"""
from typing import List
from decimal import Decimal
import numpy as np

precedence = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '^': 2
}

constants = {
    'pi': np.pi,
    'e': np.e
}

functions = {
    'sin': (np.sin, 1),
    'cos': (np.cos, 1),
    'tan': (np.tan, 1),
    'tg': (np.tan, 1),
    'cot': (lambda x: 1/np.tan(x), 1),
    # 'sec': np.sec,
    'arcsin': (np.arcsin, 1),
    'arccos': (np.arccos, 1),

    'exp': (np.exp, 1),
    'ln': (np.log, 1),
    'log': (np.log, 2)
}

names = list(functions.keys()) + list(constants.keys()) \
            + list(precedence.keys()) + [',', '(', ')']
names = sorted(names, key=lambda x: len(x), reverse=True)


def preprocess(s: str) -> List[str]:
    for idx, name in enumerate(names):
        s = s.replace(name, f' _f{idx} ')
    while "  " in s:
        s = s.replace('  ', ' ')
    if s.startswith(' '):
        s = s[1:]
    if s.endswith(' '):
        s = s[:-1]
    return s.split(' ')


def rpn(string):
    output = []
    op_queue = []
    string = preprocess(string)
    while string:
        token = string.pop(0) # read token
        # if the token is a number, then:
        #    push it to the output queue.
        if not token.startswith('_f'):
            output.append(Decimal(token))

        else:
            token = names[int(token[2:])]
            if token in constants.keys():
                output.append(Decimal(constants[token]))

            # if the token is a function then:
            #    push it onto the operator stack
            elif token in functions.keys():
                op_queue = [token] + op_queue # TODO: modify for priorities
            elif token in ['+', '-', '*', '/', '^']:
                op_queue = [token] + op_queue

            # if the token is a left paren (i.e."("), then:
            #    push it onto the operator stack.
            elif token == '(':
                op_queue = [token] + op_queue
            # if the token is a right paren (i.e.")"), then:
            #    while the operator at the top of the operator stack is not a left paren:
            #        pop the operator from the operator stack onto the output queue.
            elif token == ')':
                token = op_queue.pop(0)
                while token != '(':
                    output.append(token)
                    token = op_queue.pop(0)

                    #  / * if the stack runs out without
                    # finding a left paren, then there are mismatched parentheses. * /

                # if there is a left paren at the top of the operator stack, then:
                # pop the operator from the operator stack and discard it
                if op_queue:
                    if op_queue[0] in functions:
                        token = op_queue.pop(0)
                        output.append(token)

    # after while loop, if operator stack not null, pop everything to output queue
    output += op_queue
    op_queue = []
    return output


