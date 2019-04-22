#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import inspect


def is_magic_method(obj):

    if not inspect.ismethod(obj) or inspect.ismethoddescriptor(obj):
        return False

    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.endswith("__") and obj_name.startswith("__")


def is_private(obj):
    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.startswith("_")


class SimplePrinter:
    def __init__(self, magic_methods=False, private=False):
        self.magic_methods = magic_methods
        self.private = private

    def format_row(self, row):

        *_, final_object = row


def simpleprint(row, hide_magic=True):

    SEP = " -> "
    END = "\n"

    # try:
    # doc = inspect.getdoc(row[-1])

    *_, last = row
    # print(last)

    try:
        argspec = "(" + ", ".join(inspect.getfullargspec(last).args) + ")"
    except:
        argspec = ""

    if last.__name__.endswith("__") and last.__name__.startswith("__"):
        if hide_magic:
            return

    if argspec != "":
        return SEP.join([c.__name__ for c in row]) + argspec
    else:
        return SEP.join([c.__name__ for c in row])
    try:
        pass
        # print(inspect.signature(row[-1])[:50], file=sys.stdout)
    except (TypeError, ValueError):
        pass
