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

import importlib


def yield_subpackages(package, modules_too=True, include_tests=False, include_hidden=False):
    """
    """
    
    path=package.__path__
    prefix=package.__name__+'.'
    onerror=lambda x: None
    
    generator = pkgutil.walk_packages(path=path,prefix=prefix,onerror=onerror)
    
    
    for importer, module_name, ispkg in generator:
        
        # Covers names such as "test", "tests", "testing", ...
        if '.test' in module_name.lower() and not include_tests:
            continue
        
        if '._' in module_name.lower() and not include_hidden:
            continue
        
        try:
            module = importlib.import_module(module_name)
        except (ModuleNotFoundError, ImportError) as error:
            print(f'Could not import {module_name}. Error: {error}')
        
        if modules_too:
            yield module, module_name
        else:
            if ispkg:
                yield module, module_name


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
    # pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
    
    import pandas
    
    for module, module_name in yield_subpackages(pandas, modules_too=True):
        print(module_name)
