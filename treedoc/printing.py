#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import inspect
import pydoc
import pkgutil

# =============================================================================
# for importer, modname, ispkg in pkgutil.iter_modules(KDEpy.__path__):
#     print(importer, modname, ispkg)
# =============================================================================


def get_modules(package, recurse=False):

    print(package)
    if not hasattr(package, "__path__"):
        return

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        print(importer, modname, ispkg)
        if ispkg and recurse:
            get_modules(
                importer.find_module(modname).load_module(modname), recurse=recurse
            )


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

    first_line, rest_lines = pydoc.splitdoc(pydoc.getdoc(last))
    to_return = ""
    if argspec != "":
        to_return = (
            SEP.join([c.__name__ for c in row])
            + argspec
            + ("\n\t" + first_line if first_line else "")
        )
    else:
        to_return = SEP.join([c.__name__ for c in row]) + (
            "\n\t" + first_line if first_line else ""
        )

    return to_return + "\n"
