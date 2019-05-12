#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:13:23 2019

@author: tommy
"""

import functools
import operator

from treedoctestpackage.module2 import function_nested_outer as imported_function


def func_addition(a, b):
    """Permforms addition."""
    return operator.add(a, b)


def func_using_imported(x):
    return imported_function(x)


add_five_partial = functools.partial(func_addition, a=5)


def func_many_args(a, b=2, c=4, d=(1, 2, 3)):
    """Function with many arguments."""
    return b + c


def generator(a):
    for i in range(a):
        yield i


def wrapper(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapped


@wrapper
def func_wrapped(a, b=2):
    return a + b


class MyClass:
    def __init__(self):
        pass

    def method_bound_to_myclass(self, a, b: int, *args, c=4.2, d: int = 42, **kwargs):
        """Method docstring."""
        return a

    @classmethod
    def classmethod_bound_to_myclass(
        cls, a, b: int, *args, c=4.2, d: int = 42, **kwargs
    ):
        """Class method docstring."""
        return a

    @staticmethod
    def static_method_bound_to_myclass(
        self, a, b: int, *args, c=4.2, d: int = 42, **kwargs
    ):
        """Static method docstring."""
        return a

    def __add__(self, other):
        return type(self)()
