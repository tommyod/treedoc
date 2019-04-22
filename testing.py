# -*- coding: utf-8 -*-

"""Main module."""


def recurse_on(obj):
    return inspect.ismodule(obj) or inspect.isclass(obj)


def is_method(obj):
    return inspect.ismethoddescriptor(obj) or inspect.ismethod(obj)


def is_interesting(obj):

    funcs = [getattr(inspect, method) for method in dir(inspect) if "is" == method[:2]]

    return any([func(obj) for func in funcs])


import inspect

from collections.abc import Callable
import time


def yield_data(obj, stack=None):
    time.sleep(0.01)

    print(f"yield_data({obj}, stack={stack})")

    try:
        getattr(obj, "__name__")
    except AttributeError:
        return

    if stack is None:
        stack = []
    stack += [obj]

    yield stack

    for (name, attribute) in inspect.getmembers(obj):

        if name in ("__class__", "__doc__", "__hash__", "builtins"):
            continue

        if not is_interesting(attribute):
            continue

        # Prevent recursing into modules
        # TODO: Generalize this
        if inspect.ismodule(obj) and inspect.ismodule(attribute):
            continue
        if inspect.isclass(obj) and inspect.isclass(attribute):
            continue
        if inspect.isabstract(obj) and inspect.isabstract(attribute):
            continue
        try:
            getattr(attribute, "__name__")
        except AttributeError:
            continue

        # This prevent recursing to superclasses
        if inspect.isclass(attribute) and attribute in inspect.getmro(attribute):
            continue

        if not recurse_on(attribute):
            yield stack + [attribute]
        else:
            yield from yield_data(attribute, stack=stack)


import math
import os
import collections
import builtins

for builtin in dir(builtins):
    if builtin in (
        "Ellipsis",
        "False",
        "True",
        "None",
        "NotImplemented",
        "__import__",
        "__build_class__",
        "builtins",
    ):
        continue

    builtin = getattr(builtins, builtin)

    for row in yield_data(builtin):
        print(
            *[c.__name__ for c in row],
            # row[-1].__doc__,
            sep="->",
        )


if True:
    import pandas as pd

    for row in yield_data(pd):
        print(*[c for c in row], sep="->")
        print(*[c.__name__ for c in row], sep="->")
        print()
