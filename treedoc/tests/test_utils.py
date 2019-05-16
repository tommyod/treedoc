#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:20:49 2019

@author: tommy
"""

import operator
from collections.abc import Callable
import collections.abc
import builtins
import math
import datetime

import pytest

import treedoctestpackage
from treedoc.utils import (
    descend_from_package,
    format_signature,
    get_docstring,
    ispackage,
    resolve_str_to_obj,
    resolve_input,
    signature_from_docstring,
)


def map_itemgetter(iterable, index: int):
    """Map an itemgetter over an iterable, returning element correpoding to index."""
    getter = operator.itemgetter(index)
    for item in iterable:
        yield getter(item)


@pytest.mark.parametrize(
    "input_arg, expected",
    [
        (math.log, ("x[, base]", "x, [base=math.e]")),
        (dict.pop, ("k[,d]", None)),
        (datetime.datetime.strptime, (None,)),
    ],
)
def test_signature_from_docstring(input_arg, expected):
    """Test the function getting signature information from docstrings.
    
    Due to builtin docstrings differing on different Python versions,
    we allow several possibilities."""
    assert signature_from_docstring(input_arg) in expected


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
    assert get_docstring(func, width=12) == "This is..."

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

    assert get_docstring(func, width=16) == "Lorem Ipsum..."


class TestDescentFromPackage:
    @staticmethod
    def test_package_to_subpackages():
        """
        Test that yielding subpackages one level down works.
        """

        sub_packages = descend_from_package(treedoctestpackage, types="package")
        sub_packages = set(map_itemgetter(sub_packages, 1))

        from treedoctestpackage import subpackage, subpackage2

        assert set([subpackage, subpackage2]) == sub_packages

        # We only go one subpackage down
        from treedoctestpackage.subpackage import subsubpackage

        assert subsubpackage not in sub_packages

        # If we go down from a subpackage, we get a subsubpackage

        from treedoctestpackage import subpackage

        sub_packages = descend_from_package(subpackage, types="package")
        sub_packages = set(map_itemgetter(sub_packages, 1))
        assert set([subsubpackage]) == sub_packages

    @staticmethod
    def test_package_to_modules():
        """
        Test that yielding modules one level down works.
        """

        modules = descend_from_package(treedoctestpackage, types="module")
        modules = set(map_itemgetter(modules, 1))

        from treedoctestpackage import module, module2

        assert set([module, module2]) == modules

    @staticmethod
    def test_package_to_modules_w_private():
        """
        Test that yielding modules one level down works with hidden modules too.
        """

        modules = descend_from_package(
            treedoctestpackage, types="module", include_private=True
        )
        modules = set(map_itemgetter(modules, 1))

        from treedoctestpackage import module, module2, _hidden_module

        assert set([module, module2, _hidden_module]) == modules


class TestObjectResolution:
    @staticmethod
    @pytest.mark.parametrize(
        "input_arg, expected",
        [
            ("list", list),
            ("builtins.set", set),
            ("operator.add", operator.add),
            ("collections.abc.Callable", Callable),
            ("collections.abc", collections.abc),
            ("", builtins),
        ],
    )
    def test_resolve_str_to_obj(input_arg, expected):
        """
        Test that objects are resolved from strings as expected.
        """
        assert resolve_str_to_obj(input_arg) == expected

    @staticmethod
    def test_resolve_str_to_obj_raises():

        with pytest.raises(ImportError):
            resolve_str_to_obj("gibberish")

    @staticmethod
    @pytest.mark.parametrize(
        "input_arg, expected",
        [
            ("list dict set", [list, dict, set]),
            (["list", "dict", "set"], [list, dict, set]),
            (["list", "dict", set], [list, dict, set]),
            ([list, dict, set], [list, dict, set]),
            ("list dict", [list, dict]),
            ("list   dict ", [list, dict]),
            ("list", [list]),
        ],
    )
    def test_resolve_input(input_arg, expected):
        """
        Test that objects are resolved from inputs.
        """

        assert resolve_input(input_arg) == expected

    @staticmethod
    def test_resolve_input_raises():

        with pytest.raises(ImportError):
            resolve_input("list dict gibberish")


class TestSignature:
    """
    Class for gathering format_signature() tests. 
    Note the stripping of whitespaces in some of the tests. More info on this in PR #9.
    """

    parameters = [
        (0, ""),
        (1, "(...)"),
        (2, "(a,b,*args,c,d,**kwargs)"),
        (3, "(a,b,*args,c=4.2,d=42,**kwargs)"),
        (4, "(a,b:int,*args,c=4.2,d:int=42,**kwargs)"),
    ]

    @staticmethod
    @pytest.mark.parametrize("verbosity, expected", parameters)
    def test_keywords_annotated_defaults_args_kwargs(verbosity, expected):
        """ 
        Test that formatting signature works on a user defined function.
        """

        def myfunc1(a, b: int, *args, c=4.2, d: int = 42, **kwargs):
            return None

        assert (
            "".join(
                char for char in format_signature(myfunc1, verbosity) if char != " "
            )
            == expected
        )

    @staticmethod
    @pytest.mark.parametrize(
        "verbosity, expected", [(0, ""), (1, "()"), (2, "()"), (3, "()"), (4, "()")]
    )
    def test_empty_signature(verbosity, expected):
        """ 
        Test that formatting signature works on a user defined function with no arguments.
        """

        def myfunc2():
            return None

        assert format_signature(myfunc2, verbosity) == expected

    @staticmethod
    @pytest.mark.parametrize(
        "verbosity, expected",
        [
            (0, ""),
            (1, "(...)"),
            (2, "(self, n)"),
            (3, "(self, n=None)"),
            (4, "(self, n=None)"),
        ],
    )
    def test_builtin_class(verbosity, expected):
        """ 
        Test that formatting signature works on a built-in class.
        """
        from collections import Counter

        assert format_signature(Counter.most_common, verbosity) == expected

    @staticmethod
    @pytest.mark.parametrize("verbosity, expected", parameters)
    def test_method(verbosity, expected):
        """
        Test that formatting signature works on a method.
        """
        myclass = treedoctestpackage.MyClass()

        assert (
            "".join(
                char
                for char in format_signature(myclass.method_bound_to_myclass, verbosity)
                if char != " "
            )
            == expected
        )

    @staticmethod
    @pytest.mark.parametrize(
        "verbosity, expected",
        [
            (0, ""),
            (1, "(...)"),
            (2, "(self,a,b,*args,c,d,**kwargs)"),
            (3, "(self,a,b,*args,c=4.2,d=42,**kwargs)"),
            (4, "(self,a,b:int,*args,c=4.2,d:int=42,**kwargs)"),
        ],
    )
    def test_static_method(verbosity, expected):
        """
        Test that formatting signature works on a static method.
        """
        myclass = treedoctestpackage.MyClass()

        assert (
            "".join(
                char
                for char in format_signature(
                    myclass.static_method_bound_to_myclass, verbosity
                )
                if char != " "
            )
            == expected
        )

    @staticmethod
    @pytest.mark.parametrize("verbosity, expected", parameters)
    def test_class_method(verbosity, expected):
        """
        Test that formatting signature works on a class method.
        """
        myclass = treedoctestpackage.MyClass()

        assert (
            "".join(
                char
                for char in format_signature(
                    myclass.classmethod_bound_to_myclass, verbosity
                )
                if char != " "
            )
            == expected
        )


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
