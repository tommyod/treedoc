#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for programming the treedoc library.
"""


class PrintMixin:
    """Adds a __repr__ method."""

    # Could've used dataclasses, but they were introduced in Python 3.8

    def __repr__(self):
        """Returns a string like ClassName(a=2, b=3)."""
        args = ["{}={}".format(k, v) for k, v in self.__dict__.items()]
        return type(self).__name__ + "({})".format(", ".join(args))
