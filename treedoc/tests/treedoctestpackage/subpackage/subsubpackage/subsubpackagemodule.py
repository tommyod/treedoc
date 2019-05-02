#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:13:23 2019

@author: tommy
"""

import operator


def func_addition(a, b):
    """Permforms addition."""
    return operator.add(a, b)


def func_subtraction(a, b):
    """Permforms addition."""
    return operator.subtract(a, b)


class BinaryOperator:
    def __init__(self, operator):
        self.operator = operator

    def get_operator(self):
        return self.operator

    def set_operator(self, operator):
        self.operator = operator
