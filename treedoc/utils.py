#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for traversal and printing.
"""

import collections
import collections.abc
import functools
import importlib
import inspect
import os
import pkgutil
import pydoc
import textwrap
import collections

_marker = object()


class PrintMixin:
    def __repr__(self):
        """Returns a string like ClassName(a=2, b=3)."""
        args = ["{}={}".format(k, v) for k, v in self.__dict__.items()]
        return type(self).__name__ + "({})".format(", ".join(args))


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


def clean_object_stack(stack):
    """
    Join an object stack so that consequtive modules are merged into the last one.
    
    This avoids the stack [collections, collections.abc] as being named
    'collections.collections.abc'.
    
    >>> import collections
    >>> from collections import abc
    >>> clean_object_stack([collections, abc]) == [abc]
    True
    >>> from collections import Counter
    >>> input_stack = [collections, Counter, Counter.most_common]
    >>> clean_object_stack(input_stack) == input_stack
    True
    """
    assert isinstance(stack, list)

    stack = stack.copy()
    new_stack = []
    for obj in stack:
        # This one is a module, and the last one is a module
        # Therefore it must be a submodule, get rid of the first one
        # to avoid [collections, collections.abc]
        if new_stack and inspect.ismodule(obj) and inspect.ismodule(new_stack[-1]):
            new_stack.pop()
        new_stack.append(obj)

    assert len(new_stack) > 0
    return new_stack


def is_inspectable(obj):
    """An object is inspectable if it returns True for any of the inspect.is.. functions."""
    funcs = (func_name for func_name in dir(inspect) if func_name.startswith("is"))
    funcs = (getattr(inspect, func_name) for func_name in funcs)
    return any([func(obj) for func in funcs]) or isinstance(obj, functools.partial)


def ispropersubpackage(package_a, package_b):
    """
    Is A a proper subpackage or submodule of B?
    """
    try:
        path_a, _ = os.path.split(inspect.getfile(package_a))
        path_b, _ = os.path.split(inspect.getfile(package_b))
        # is a built-in module
    except TypeError:
        return False

    return (path_b in path_a) and not (path_b == path_a)


def issubpackage(package_a, package_b):
    """
    Is A a subpackage or submodule of B?
    """
    try:
        path_a, _ = os.path.split(inspect.getfile(package_a))
        path_b, _ = os.path.split(inspect.getfile(package_b))
        # is a built-in module
    except TypeError:
        return False

    return path_b in path_a


def is_dunder_method(obj):
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
    """ 
    Checks if signature.Parameter corresponds to *args or **kwargs type input.
    """
    if (
        param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
        and param.default is param.empty
    ):
        return str(param)
    else:
        return param.name


def _between(string, start, end):
    """Returns what's between `start` and `end`, exclusive.
    
    Examples
    >>> _between("im a nice (person) to all", "(", ")")
    'person'
    >>> _between("im a nice (person to all", "(", ")")
    Traceback (most recent call last):
        ...
    ValueError: substring not found
    """
    i = string.index(start)
    part = string[i + len(start) :]
    j = part.index(")")
    return part[:j]


def signature_from_docstring(obj):
    """Extract signature from built-in object docstring.
    
    Some of the built-in methods have signature info in the docstring. One example is
    `dict.pop`. This method will retrieve the docstring, and return None if it cannot.
    
    >>> import math
    >>> signature_from_docstring(math.log) in ('x[, base]', 'x, [base=math.e]')
    True
    >>> signature_from_docstring(dict.pop) in ('k[,d]', None)
    True
    """

    # If not docstring is available, return
    docstring_line = get_docstring(obj)
    if not docstring_line:
        return None

    # If it's not callable, return
    if not isinstance(obj, collections.abc.Callable):
        return None

    # Look for the name of the object, i.e. func(x)
    assert hasattr(obj, "__name__")
    if not obj.__name__ in docstring_line:
        return None

    # Attempt to get the signature
    signature_part = docstring_line[len(obj.__name__) :]
    try:
        return _between(signature_part, "(", ")")
    except ValueError:
        return None


def format_signature(obj, verbosity=2):
    """ 
    Format a function signature for printing.
    
    This function tries first to use inspect.signature, if that fails it will look for
    signature information in the first line of the docstring, and if that fails it will
    return a generic sigature if the object is callable.
    
    Examples
    --------
    >>> import collections
    >>> # Works on functions with well-defined signature
    >>> format_signature(collections.defaultdict.fromkeys, verbosity=2)
    '(iterable, value)'
    >>> # Built-ins with signature information in the docs
    >>> format_signature(collections.defaultdict.update, verbosity=2)
    '([E, ]**F)'
    >>> # Built-ins with signature no signature information at all
    >>> format_signature(collections.deque.append, verbosity=2)
    '(...)'
    """
    # TODO: Figure out how to handle *

    max_verbosity = 4
    assert 0 <= verbosity <= max_verbosity
    SEP = ", "

    # Return formatted signature based on verbosity
    if verbosity == 0:
        return ""

    # Check if object has signature
    try:
        sig = inspect.signature(obj)
    except ValueError:
        # inspect.signature raises ValueError if no signature can be provided.
        # Example:
        # -------
        # >>> inspect.signature(math.log)
        # 'ValueError: no signature found for builtin <built-in function log>'

        signature_in_docs = signature_from_docstring(obj)

        # Failed to find a signature in the docstring
        if signature_in_docs is None:

            # inspect.signature and docstring info has failed, still return if callable
            if isinstance(obj, collections.abc.Callable) and verbosity >= 1:
                return "(...)"
            return ""

        # Found a signature in the docstring
        else:
            if verbosity == 1:
                return "(...)"
            else:
                # TODO: Format this more depending on verbosity
                return "(" + signature_in_docs + ")"
        return ""

    except TypeError:
        # inspect.signature raises TypeError if type of object is not supported.
        # Example:
        # -------
        # >>> x = 1
        # >>> inspect.signature(x)
        # 'TypeError: 1 is not a callable object'
        return ""

    # If function as no arguments, return
    if str(sig) == "()" and verbosity > 0:
        return str(sig)

    # Check if signature has annotations or defaults
    annotated = any(
        param.annotation is not param.empty for param in sig.parameters.values()
    )
    has_defaults = any(
        param.default is not param.empty for param in sig.parameters.values()
    )

    # Dial down verbosity if user has provided a more verbose alternative than is available
    if not annotated:
        max_verbosity = 3

    if not has_defaults and not annotated:
        max_verbosity = 2

    if verbosity > max_verbosity:
        # TODO: Give user warning if verbosity needs to be adjusted, e.g.
        # print(f'Adjusting verbosity: {verbosity} -> {max_verbosity}.')
        verbosity = max_verbosity

        # Fails for instance on collections.ChainMap without this
        return str(sig)

    elif verbosity == 1:
        return "(...)"

    elif verbosity == 2:
        return (
            "(" + SEP.join(_get_name(param) for param in sig.parameters.values()) + ")"
        )

    elif verbosity == 3:
        return (
            "("
            + SEP.join(
                param.name + "=" + str(param.default)
                if param.default is not param.empty
                else _get_name(param)
                for param in sig.parameters.values()
            )
            + ")"
        )

    else:
        return str(sig)


def descend_from_package(
    package, types="package", include_tests=False, include_hidden=False
):
    """
    Descent from a package to either a subpackage or modules one level down.
    
    Yields a tuple of (object, object_name) one level down.
    """
    if not inspect.ismodule(package):
        return None

    try:
        path, _ = os.path.split(inspect.getfile(package))
        # TypeError: <module 'itertools' (built-in)> is a built-in module
    except TypeError:
        return None

    prefix = package.__name__ + "."

    generator = pkgutil.iter_modules(path=[path], prefix=prefix)

    for (importer, object_name, ispkg) in generator:

        ismodule = not ispkg

        # Covers names such as "test", "tests", "testing", ...
        if ".test" in object_name.lower() and not include_tests:
            continue

        if "._" in object_name.lower() and not include_hidden:
            continue

        try:
            obj = importlib.import_module(object_name)
        except ModuleNotFoundError:
            # TODO: Replace this with logging
            # print(f"Could not import {object_name}. Error: {error}")
            return
        except ImportError:
            # print(f"Could not import {object_name}. Error: {error}")
            return

        if types.lower() == "package" and ispkg:
            yield object_name, obj
        elif types.lower() == "module" and ismodule:
            yield object_name, obj
        elif types.lower() == "both":
            yield object_name, obj
        elif types.lower() not in ("package", "module", "both"):
            raise ValueError("Parameter `types` must be 'package', 'module' or 'both'.")


def resolve_str_to_obj(object_string):
    """
    Resolve a string to a Python object.
    
    
    list -> builtin
    collections -> module
    collections.Counter -> object
    
    Examples
    --------
    >>> resolve_str_to_obj("list") == list
    True
    >>> import collections
    >>> resolve_str_to_obj("collections") == collections
    True
    >>> from collections import Counter
    >>> resolve_str_to_obj("collections.Counter") == Counter
    True
    >>> resolve_str_to_obj("gibberish.Counter")
    Traceback (most recent call last):
        ...
    ImportError: Could not resolve 'gibberish.Counter'.
    """
    assert isinstance(object_string, str)
    suggestion = pydoc.locate(object_string)

    if suggestion is None and object_string != "None":
        raise ImportError("Could not resolve '{}'.".format(object_string))
    else:
        return suggestion


def resolve_input(obj):
    """Resolve a general input (str, iterable, etc) to a list of Python objects.
    
    
    Examples
    --------
    >>> resolve_input("list") == [list]
    True
    >>> resolve_input("list dict") == [list, dict]
    True
    >>> len(resolve_input("python")) > 10
    True
    >>> resolve_input(["list"]) == [list]
    True
    >>> resolve_input(["list", "dict"]) == [list, dict]
    True
    >>> from collections.abc import Collection
    >>> resolve_input("collections.abc.Collection") == [Collection]
    True
    """
    if isinstance(obj, str):
        obj = obj.strip()

    if isinstance(obj, str) and " " in obj:
        # Parse "dict   str  " correctly, ignoring extra whitespace
        obj = [o for o in obj.split(" ") if o != ""]

    # Special handling if "python" is passed
    if isinstance(obj, str) and obj.lower().strip() == "python":
        objects = []

        for (importer, object_name, ispkg) in pkgutil.iter_modules():

            if not ispkg:
                continue

            try:
                obj = importlib.import_module(object_name)
            except:
                continue

            objects.append(object)

        return objects

    elif isinstance(obj, str):
        assert " " not in obj
        return [resolve_str_to_obj(obj)]

    elif isinstance(obj, (list, set, tuple)):
        attempt = [resolve_str_to_obj(o) if isinstance(o, str) else o for o in obj]
        return [obj for obj in attempt if obj is not None]

    else:
        raise ValueError("Could not resolve object")


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
