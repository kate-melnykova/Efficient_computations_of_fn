from decimal import Decimal
from decimal import getcontext
import unittest
from unittest import TestCase
from operator import add, sub, mul, truediv

import numpy as np

precision = 8
getcontext().prec = precision
constants = {'pi': str(Decimal(np.pi)),
             'e': str(Decimal(np.e))
             }


def compute_algebraic(s: str):
    dic = {'+': add,
           '-': sub,
           '*': mul,
           '/': truediv
           }

    for symb in ['+', '-', '*', '/']:
        if symb in s:
            [clause1, clause2] = s.split(symb, maxsplit=1)
            if not clause1:
                clause1 = 0
            operation = dic[symb]
            return operation(compute(clause1), compute(clause2))
    raise
    # TODO: specify error


def exclude_brackets(s):
    if '(' in s:
        print('Removing brackets from: ', s)
        # find matching bracket
        i0 = s.index('(')
        balance = 1
        for i in range(i0+1, len(s)):
            if s[i] == '(':
                balance += 1
            elif s[i] == ')':
                balance -= 1
            if not balance:
                break
        assert not balance
        clause = s[i0+1:i]
        s_new = str(compute(clause))
        print(f'Clause={clause}, resulting value={s_new}')
        if i0 > 0:
            s_new = s[0:i0] + s_new
        if i < len(s)-2:
            s_new += s[i+1:]
        print('Returning string: ', s_new)
        return s_new
    else:
        return s


def compute(s):
    s = str(s)
    s = s.replace(' ', '')

    # exclude brackets
    while '(' in str(s):
        s = exclude_brackets(s)

    # replace constants with numbers
    # TODO add constant analysis
    for k, v in constants.items():
        s = s.replace(k, v)
    print(f'After removing constants = {s}')

    # perform basic algebraic manipulations
    dic = {'+': add,
           '-': sub,
           '*': mul,
           '/': truediv
           }

    if '+' in s or '-' in s or '*' in s or '/' in s:
        return compute_algebraic(s)

    print(f's should be number, and is {s}')
    return Decimal(s)


class TestCalc(TestCase):
    def test_one_step_algebra(self):
        self.assertEqual(compute('2+3'), Decimal('5'))
        self.assertEqual(compute('4-7.4'), Decimal('-3.4'))
        self.assertEqual(compute('6*0'), Decimal('0'))
        self.assertEqual(compute('1/4'), Decimal('0.25'))

    def test_multi_step_algebra(self):
        self.assertEqual(compute('2+3+6'), Decimal('11'))
        self.assertEqual(compute('1-5+5'), Decimal('1'))
        self.assertEqual(compute('1*8-3'), Decimal('5'))
        self.assertEqual(compute('1+8/2'), Decimal('5'))

    def test_with_brackets(self):
        self.assertEqual(compute('2+(4-5)'), Decimal('1'))
        self.assertEqual(compute('4*(9-7)'), Decimal('8'))
        self.assertEqual(compute('(3-2)*(7+4)'), Decimal('11'))
        self.assertEqual(compute('(3*(2*(5-4)))'), Decimal('6'))

    def test_with_constant(self):
        self.assertAlmostEqual(compute('pi'), Decimal(str(np.pi)), places=precision-1)
        self.assertAlmostEqual(compute('pi+1'), Decimal(str(np.pi + 1)), places=precision-1)
        self.assertAlmostEqual(compute('pi+e'), Decimal(str(np.pi + np.e)), places=precision-1)
        self.assertAlmostEqual(compute('(pi + 3)/(e-1)'), Decimal(str((np.pi+3) / (np.e-1))), places=precision-2)


if __name__ == '__main__':
    unittest.main()

