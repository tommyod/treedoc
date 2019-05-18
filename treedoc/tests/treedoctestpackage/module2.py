#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:13:23 2019

@author: tommy
"""
import functools


def function_nested_outer(x):
    def function_nested_inner(x):
        return x

    return function_nested_inner


def function_with_inner_class(x):
    class ClassInsideFunction:
        pass

    return x


def function_which_will_become_staticmethod():
    pass


def wrapper(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapped


@wrapper
def func_wrapped(a, b=2):
    return a + b


# =============================================================================
# CLASSES AND INHERITANCE
# =============================================================================


class SuperClass:
    def superclass_method(self):
        return 1

    static_method = staticmethod(function_which_will_become_staticmethod)


class SubClass(SuperClass):
    def subclass_method(self):
        return 1


class SubSubClass(SubClass):
    def subsubclass_method(self):
        return 1


# =============================================================================
# CLASSES WITH COMPOSITION
# =============================================================================


class Wheel:
    pass


class Car:

    wheel_cls = Wheel
    wheel = Wheel()
