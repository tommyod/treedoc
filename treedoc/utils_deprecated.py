#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions which are not in use.
"""

import inspect


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


def inspect_classify(obj):
    """
    Classify an object according to the inspect module. Not disjoint.
    
    Examples
    --------
    >>> inspect_classify(list)
    ['class']
    >>> f = lambda x : x * x
    >>> inspect_classify(f)
    ['function', 'routine']
    >>> class Vector:
    ...     def add(self, other):
    ...         pass
    >>> inspect_classify(Vector)
    ['class']
    >>> inspect_classify(Vector.add)
    ['function', 'routine']
    >>> gen = (i for i in range(10))
    >>> inspect_classify(gen)
    ['generator']
    >>> inspect_classify(max)
    ['builtin', 'routine']
    
    
    Common findings:
        []
        ['abstract', 'class']
        ['builtin', 'routine']
        ['class']
        ['datadescriptor']
        ['datadescriptor', 'getsetdescriptor']
        ['datadescriptor', 'memberdescriptor']
        ['function', 'generatorfunction', 'routine']
        ['function', 'routine']
        ['methoddescriptor', 'routine']
        ['method', 'routine']
        ['module']
        
        Numpy ufuncs not found.
    """
    classes = list()

    for function_name in sorted(dir(inspect)):

        if not function_name.startswith("is"):
            continue

        function = getattr(inspect, function_name)

        if function(obj):
            classes.append(function_name[2:])

    return classes


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
