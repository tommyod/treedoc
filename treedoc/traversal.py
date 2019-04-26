#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recursive traversal of objects.
"""

import functools
import inspect
import time

time = time


def pprint(*args, **kwargs):
    return None
    print(*args, **kwargs)


def recurse_on(obj):
    return inspect.ismodule(obj) or inspect.isclass(obj)


def is_method(obj):
    return inspect.ismethoddescriptor(obj) or inspect.ismethod(obj)


def is_bound_method(obj):
    condition1 = "." in obj.__qualname__
    if not inspect.getfullargspec(obj).args:
        return False
    condition2 = inspect.getfullargspec(obj).args[0] == "self"
    return condition1 and condition2


def is_interesting(obj):
    funcs = [getattr(inspect, method) for method in dir(inspect) if "is" == method[:2]]
    return any([func(obj) for func in funcs]) or isinstance(obj, functools.partial)


class ObjectTraverser:
    def __init__(self):
        pass

    def search(self, obj, stack=None, key=None):
        """
        """
        # time.sleep(0.001)

        pprint(f"yield_data({obj}, stack={stack})")

        try:
            getattr(obj, "__name__")
        except AttributeError:
            return

        if stack is None:
            stack = []
        stack.append(obj)

        yield stack

        for name, attribute in sorted(inspect.getmembers(obj), key=key):

            # time.sleep(0.001)
            pprint(f"Looking at {name}, {type(attribute)}")

            if name in ("__class__", "__doc__", "__hash__", "builtins"):
                continue

            if not is_interesting(attribute):
                pprint(f" {name} was not interesting")
                continue

            # Prevent recursing into modules
            # TODO: Generalize this

            if inspect.ismodule(obj) and inspect.ismodule(attribute):
                pprint(f" Both {name} and {obj.__name__} are modules")
                continue
                # If it's not the same package, skip it
                if attribute.__package__ != obj.__package__:
                    pprint(
                        f" Both {attribute.__package__} and {obj.__package__} are modules"
                    )
                    continue

            if inspect.isclass(obj) and inspect.isclass(attribute):
                continue
            if inspect.isabstract(obj) and inspect.isabstract(attribute):
                continue

            if inspect.isclass(attribute) and inspect.getmodule(attribute) != obj:
                print(f"{name} - {attribute.__module__}")
                continue

            if (
                inspect.isfunction(attribute)
                and not is_bound_method(attribute)
                and inspect.getmodule(attribute) != obj
            ):

                # print(f"{name} - {attribute.__module__}")
                continue

                # print(f"{obj.__name__} - {obj.__module__}")

            try:
                getattr(attribute, "__name__")
            except AttributeError:
                try:
                    setattr(attribute, "__name__", name)
                except AttributeError:
                    continue

            # This prevent recursing to superclasses
            if inspect.isclass(attribute):
                pprint(
                    f" The MRO of {name} is {inspect.getmro(attribute)}. Parent is {obj.__name__}"
                )
                pprint(f"{name} is a class: {inspect.isclass(attribute)}")
                pprint(f"{obj.__name__} is a class: {inspect.isclass(obj)}")
            if inspect.isclass(attribute) and obj in inspect.getmro(attribute):
                continue

            if not recurse_on(attribute):
                pprint(f" Not recursing on {name}")
                yield stack + [attribute]
            else:
                yield from self.search(obj=attribute, stack=stack)

        stack.pop()


if __name__ == "__main__":

    import KDEpy

    from printing import simpleprint

    objtrav = ObjectTraverser()
    for row in objtrav.search(KDEpy):

        print(simpleprint(row))

        # print(row[-1].__doc__)

        # print(*[c for c in row], sep="->")
        # print(*[c.__name__ for c in row], sep="->")
        # print(*[type(c) for c in row], sep="->")
        # print()
