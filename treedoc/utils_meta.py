#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for programming the treedoc library.
"""
import functools


class PrintMixin:
    """Adds a __repr__ method."""

    # Could've used dataclasses, but they were introduced in Python 3.8

    def __repr__(self):
        """Returns a string like ClassName(a=2, b=3)."""
        args = ["{}={}".format(k, v) for k, v in self.__dict__.items()]
        return type(self).__name__ + "({})".format(", ".join(args))


def ensure_output(out_type):
    """Returns a function which takes in a function and ensures its output type."""

    def verify_func_out(function):
        """Returns a new function where the output type is ensured."""

        @functools.wraps(function)
        def new_func(*args, **kwargs):
            output = function(*args, **kwargs)
            if not isinstance(output, out_type):
                args = function.__name__, out_type
                raise TypeError("Output of {} must be of type {}".format(*args))
            return output

        return new_func

    return verify_func_out
