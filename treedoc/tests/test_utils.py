#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:20:49 2019

@author: tommy
"""

import operator

import treedoctestpackage
from treedoc.utils import descend_from_package, ispackage, resolve_object, get_docstring


def map_itemgetter(iterable, index):
    getter = operator.itemgetter(index)
    for item in iterable:
        yield getter(item)


def test_ispackage():

    import treedoctestpackage

    assert ispackage(treedoctestpackage)

    from treedoctestpackage import subpackage

    assert ispackage(subpackage)

    from treedoctestpackage import module

    assert not ispackage(module)

    from treedoctestpackage.subpackage import subpackagemodule

    assert not ispackage(subpackagemodule)


def test_get_docstring():
    """Test retrieval of docstrings."""

    def func():
        pass

    return_val = "This is the docstring."

    func.__doc__ = """This is the docstring."""
    assert get_docstring(func) == return_val

    func.__doc__ = """
    
    
    This is the docstring.
    
    
    """
    assert get_docstring(func) == return_val

    func.__doc__ = """
    This is the docstring.
    
    This is more stuff.
    """
    assert get_docstring(func) == return_val

    func.__doc__ = """
    This is the docstring. More information here.
    
    Even more stuff.
    """
    assert get_docstring(func) == "This is the docstring. More information here."
    assert get_docstring(func, 12) == "This is..."

    delattr(func, "__doc__")
    assert get_docstring(func) == ""

    func.__doc__ = """
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
    when an unknown printer took a galley of type and scrambled it to make a type 
    specimen book. It has survived not only five centuries, but also the leap into 
    electronic typesetting, remaining essentially unchanged. It was popularised 
    in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
    and more recently with desktop publishing software like Aldus PageMaker 
    including versions of Lorem Ipsum.
    """

    assert get_docstring(func, 16) == "Lorem Ipsum..."


class TestDescentFromPackage:
    @staticmethod
    def test_package_to_subpackages():
        """
        Test that yielding subpackages one level down works.
        """

        sub_packages = descend_from_package(treedoctestpackage, types="package")
        sub_packages = set(map_itemgetter(sub_packages, 0))

        from treedoctestpackage import subpackage, subpackage2

        assert set([subpackage, subpackage2]) == sub_packages

        # We only go one subpackage down
        from treedoctestpackage.subpackage import subsubpackage

        assert subsubpackage not in sub_packages

        # If we go down from a subpackage, we get a subsubpackage

        from treedoctestpackage import subpackage

        sub_packages = descend_from_package(subpackage, types="package")
        sub_packages = set(map_itemgetter(sub_packages, 0))
        assert set([subsubpackage]) == sub_packages

    @staticmethod
    def test_package_to_modules():
        """
        Test that yielding modules one level down works.
        """

        modules = descend_from_package(treedoctestpackage, types="module")
        modules = set(map_itemgetter(modules, 0))

        from treedoctestpackage import module, module2

        assert set([module, module2]) == modules

    @staticmethod
    def test_package_to_modules_w_hidden():
        """
        Test that yielding modules one level down works with hidden modules too.
        """

        modules = descend_from_package(
            treedoctestpackage, types="module", include_hidden=True
        )
        modules = set(map_itemgetter(modules, 0))

        from treedoctestpackage import module, module2, _hidden_module

        assert set([module, module2, _hidden_module]) == modules


def test_resolve_object():
    """
    Test that objects are resolved from strings as expected.
    """

    assert resolve_object("None") == None
    assert resolve_object("list") == list
    assert resolve_object("builtins.set") == set
    assert resolve_object("operator.add") == operator.add
    assert resolve_object("operator") == operator
    assert resolve_object("Python") == None

    from collections.abc import Callable

    assert resolve_object("collections.abc.Callable") == Callable

    import collections.abc as module

    assert resolve_object("collections.abc") == module


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
