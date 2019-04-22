#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import inspect
import sys
import io


def simpleprint(row, hide_magic=True):

    SEP = "->"
    END = "\n"

    # try:
    # doc = inspect.getdoc(row[-1])

    *_, last = row
    # print(last)

    if last.__name__.endswith("__") and last.__name__.startswith("__"):
        if hide_magic:
            return

    return SEP.join([c.__name__ for c in row])
    try:
        pass
        # print(inspect.signature(row[-1])[:50], file=sys.stdout)
    except (TypeError, ValueError):
        pass
