#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for traversal and printing.
"""

import collections
import functools
import importlib
import inspect
import os
import pkgutil
import pydoc
import textwrap

_marker = object()


class Peekable:
    """Wrap an iterator to allow a lookahead.
    
    Call `peek` on the result to get the value that will be returned by `next`. 
    This won't advance the iterator:
        
    >>> p = Peekable(['a', 'b'])
    >>> p.peek()
    'a'
    >>> next(p)
    'a'
        
    Pass `peek` a default value to return that instead of raising ``StopIteration`` 
    when the iterator is exhausted.
    
    >>> p = Peekable([])
    >>> p.peek('hi')
    'hi'

    """

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = collections.deque()

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self, default=_marker):
        """Return the item that will be next returned from ``next()``.
        
        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.
        """
        if not self._cache:
            try:
                self._cache.append(next(self._it))
            except StopIteration:
                if default is _marker:
                    raise
                return default
        return self._cache[0]

    def __next__(self):
        if self._cache:
            return self._cache.popleft()

        return next(self._it)


def get_docstring(object, width=88):
    """Get a docstring summary from an object.
    
    If no docstring is available, an empty string is returned.
    
    Examples
    --------
    >>> get_docstring(set.intersection)
    'Return the intersection of two sets as a new set.'
    >>> get_docstring(set.intersection, width=18)
    'Return the...'
    """
    # pydoc.getdoc is slightly more general than inspect.getdoc,see:
    # https://github.com/python/cpython/blob/master/Lib/pydoc.py#L92
    doc = pydoc.getdoc(object)
    first_line, _ = pydoc.splitdoc(doc)

    return_value = textwrap.shorten(first_line, width=width, placeholder="...")
    if return_value:
        return return_value

    # If the docstring is a long paragraph, pydoc.splitdoc will return ''
    # We change this behavior to include the start of the string.
    if not return_value and doc:
        return textwrap.shorten(doc, width=width, placeholder="...")

    return ""


_marker = object()


class Peekable:
    """Wrap an iterator to allow a lookahead.
    
    Call `peek` on the result to get the value that will be returned by `next`. 
    This won't advance the iterator:
        
    >>> p = Peekable(['a', 'b'])
    >>> p.peek()
    'a'
    >>> next(p)
    'a'
        
    Pass `peek` a default value to return that instead of raising ``StopIteration`` 
    when the iterator is exhausted.
    
    >>> p = Peekable([])
    >>> p.peek('hi')
    'hi'

    """

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = collections.deque()

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self, default=_marker):
        """Return the item that will be next returned from ``next()``.
        
        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.
        """
        if not self._cache:
            try:
                self._cache.append(next(self._it))
            except StopIteration:
                if default is _marker:
                    raise
                return default
        return self._cache[0]

    def __next__(self):
        if self._cache:
            return self._cache.popleft()

        return next(self._it)


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


def is_inspectable(obj):
    """An object is inspectable if it returns True for any of the inspect.is.. functions."""
    funcs = (func_name for func_name in dir(inspect) if func_name.startswith("is"))
    funcs = (getattr(inspect, func_name) for func_name in funcs)
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


def _get_name(param):
    ''' Checks if signature.Parameter corresponds to *args or **kwargs type input.'''
    if param.kind in (param.KEYWORD_ONLY, param.VAR_KEYWORD) and param.default is param.empty:
        return str(param)
    else:
        return param.name
    

def format_signature(obj, verbosity=2):
    ''' Format a function signature for printing.'''
    # TODO: Figure out how to handle *
    
    max_verbosity = 4
    assert 0 <= verbosity <= max_verbosity
    SEP = ', '
    
    # Check if object has signature
    try:
        sig = inspect.signature(obj)
    except ValueError as error:
        print(error)
        return
    except TypeError:
        raise
        
    # If function as no arguments, return
    if str(sig) == '()' and verbosity > 0:
        return str(sig)
    
    # Check if signature has annotations or defaults
    annotated = any(param.annotation is not param.empty for param in sig.parameters.values())
    has_defaults = any(param.default is not param.empty for param in sig.parameters.values())

    # Dial down verbosity if user has provided a more verbose alternative than is available
    if not annotated:
        max_verbosity = 3
    
    if not has_defaults and not annotated:
        max_verbosity = 2
        
    if verbosity > max_verbosity:
        # TODO: Give user warning if verbosity needs to be adjusted, e.g.
        # print(f'Adjusting verbosity: {verbosity} -> {max_verbosity}.')
        verbosity = max_verbosity
    
    # Return formatted signature based on verbosity
    if verbosity == 0:
        return ''
    
    elif verbosity == 1:
        return '(...)'
    
    elif verbosity == 2:
        return '(' + SEP.join(_get_name(param) for param in sig.parameters.values()) + ')'

    elif verbosity == 3:
        return '(' + SEP.join(
            param.name + '=' + str(param.default) 
            if param.default is not param.empty
            else _get_name(param)
            for param in sig.parameters.values()
        ) + ')'
    
    else:
        return str(sig)


def descend_from_package(
    package, types="package", include_tests=False, include_hidden=False
):
    """
    Descent from a package to either a subpackage or modules on level down.
    
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
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
