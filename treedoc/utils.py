#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:53:47 2019

@author: tommy
"""

import pydoc
import pkgutil


import treedoctestpackage
import treedoc
import collections.abc

import importlib
import inspect


def is_magic_method(obj):
    #if not inspect.ismethod(obj) or inspect.ismethoddescriptor(obj) or isinstance(obj, collections.abc.Callable):
    #    return False

    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.endswith("__") and obj_name.startswith("__")


def is_private(obj):
    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.startswith("_") and obj_name[1] != '_'


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