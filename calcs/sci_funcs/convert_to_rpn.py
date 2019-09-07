"""
convert infix notation to rpn
"""
from typing import List
from decimal import Decimal
import math

precedence = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 2,
    '--': 3,
    '^': 4
}

constants = {
    'pi': math.pi,
    'e': math.e
}

functions = {
    'sin': (math.sin, 1),
    'cos': (math.cos, 1),
    'tan': (math.tan, 1),
    'tg': (math.tan, 1),
    'cot': (lambda x: 1/math.tan(x), 1),
    # 'sec': np.sec,
    'arcsin': (math.asin, 1),
    'arccos': (math.acos, 1),

    'exp': (math.exp, 1),
    'ln': (math.log, 1),
    'log': (math.log, 2)
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
    token = None
    while string:
        prev_token = token
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
                op_queue = [token] + op_queue
            elif token in ['+', '-', '*', '/', '^']:
                # check if it is unary minus or plus
                if token in ['+', '-'] and (prev_token is None
                                            or prev_token in functions
                                            or prev_token in ['+', '-', '*', '/', '^']
                                            or prev_token == '('):
                    if token == '-':
                        op_queue = ['--'] + op_queue
                else:
                    # consider precedence
                    token_prec = precedence[token]
                    while op_queue:
                        if op_queue[0] in ['+', '-', '*', '/', '^', '--']:
                            if precedence[op_queue[0]] > token_prec:
                                token_temp = op_queue.pop(0)
                                output.append(token_temp)
                            else:
                                break
                        else:
                            break
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
                token = ')'

    # after while loop, if operator stack not null, pop everything to output queue
    output += op_queue
    op_queue = []
    return output


