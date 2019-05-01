#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for traversal and printing.
"""

import functools
import importlib
import inspect
import os
import pkgutil
import pydoc


def pprint(*args, **kwargs):
    return None
    print(*args, **kwargs)


def recurse_on(obj):
    """The objects we recurse on."""
    return inspect.ismodule(obj) or inspect.isclass(obj)


def is_method(obj):
    """Whether an object is a method or not."""
    return inspect.ismethoddescriptor(obj) or inspect.ismethod(obj)


def is_bound_method(obj):
    """Whether a method is bound to a class or not."""
    condition1 = "." in obj.__qualname__
    if not inspect.getfullargspec(obj).args:
        return False
    condition2 = inspect.getfullargspec(obj).args[0] == "self"
    return condition1 and condition2


def is_inspectable(obj):
    """An object is inspectable if it returns True for any of the inspect.is.. functions."""
    funcs = (getattr(inspect, method) for method in dir(inspect) if "is" == method[:2])
    return any([func(obj) for func in funcs]) or isinstance(obj, functools.partial)


def ispropersubpackage(package_a, package_b):
    """
    Is A a subpackage or submodule of B?
    """
    try:
        path_a, _ = os.path.split(inspect.getfile(package_a))

        # is a built-in module
    except TypeError:
        return False

    path_b, _ = os.path.split(inspect.getfile(package_b))
    return (path_b in path_a) and not (path_b == path_a)


def is_magic_method(obj):
    # if not inspect.ismethod(obj) or inspect.ismethoddescriptor(obj) or isinstance(obj, collections.abc.Callable):
    #    return False

    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.endswith("__") and obj_name.startswith("__")


def is_private(obj):
    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    typical_private = obj_name.startswith("_") and obj_name[1] != "_"
    private_subpackage = "._" in obj_name
    return typical_private or private_subpackage


def ispackage(obj):

    if not hasattr(obj, "__file__"):
        return False

    return obj.__file__.endswith("__init__.py")


def descend_from_package(
    package, types="package", include_tests=False, include_hidden=False
):
    """
    Descent from a package to either a sub-package or modules on level down.
    
    Yields a tuple of (object, object_name) one level down.
    """

    path = package.__path__
    prefix = package.__name__ + "."

    generator = pkgutil.iter_modules(path=path, prefix=prefix)

    for (importer, object_name, ispkg) in generator:

        ismodule = not ispkg

        # Covers names such as "test", "tests", "testing", ...
        if ".test" in object_name.lower() and not include_tests:
            continue

        if "._" in object_name.lower() and not include_hidden:
            continue

        try:
            obj = importlib.import_module(object_name)
        except (ModuleNotFoundError, ImportError) as error:
            # TODO: Replace this with logging
            print(f"Could not import {object_name}. Error: {error}")

        if types.lower() == "package" and ispkg:
            yield obj, object_name
        elif types.lower() == "module" and ismodule:
            yield obj, object_name
        elif types.lower() == "both":
            yield obj, object_name
        elif types.lower() not in ("package", "module", "both"):
            raise ValueError("Parameter `types` must be 'package', 'module' or 'both'.")


def resolve_object(object_string):
    """
    Resolve a string to a Python object.
    
    
    list -> builtin
    collections -> module
    collections.Counter -> object
    
    Examples
    --------
    >>> resolve_object("list") == list
    True
    >>> import collections
    >>> resolve_object("collections") == collections
    True
    >>> from collections import Counter
    >>> resolve_object("collections.Counter") == Counter
    True
    >>> resolve_object("gibberish.Counter") is None
    True
    """
    assert isinstance(object_string, str)
    return pydoc.locate(object_string)


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
