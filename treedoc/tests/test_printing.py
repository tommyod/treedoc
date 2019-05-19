#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for classes and functions located in `printing.py`.
"""

import builtins
import collections.abc
import datetime
import itertools
import math
import operator
from collections.abc import Callable

import pytest

import treedoctestpackage
from treedoc.printing import (
    TreePrinter,
    format_signature,
    get_docstring,
    resolve_input,
    resolve_str_to_obj,
    signature_from_docstring,
)
from treedoc.utils import Peekable


class TestTreePrinterRowFormatting:
    def test_row_formatting_ex1(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        # These can be substituted for further generalization.
        # TODO
        # =============================================================================
        #         RIGHT = "├──"
        #         DOWN = "│  "
        #         LAST = "└──"
        #         BLANK = "   "
        # =============================================================================

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "A", "a"], [True, False, False]),
            (["root", "A", "b"], [True, False, False]),
            (["root", "A", "c"], [True, False, True]),
            (["root", "B"], [True, True]),
            (["root", "B", "a"], [True, True, False]),
            (["root", "B", "b"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "│  ", "├──"], ["root", "A", "a"]),
            (["", "│  ", "├──"], ["root", "A", "b"]),
            (["", "│  ", "└──"], ["root", "A", "c"]),
            (["", "└──"], ["root", "B"]),
            (["", "   ", "├──"], ["root", "B", "a"]),
            (["", "   ", "└──"], ["root", "B", "b"]),
        ]

    def test_row_formatting_ex2(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "A", "a"], [True, False, False]),
            (["root", "A", "b"], [True, False, True]),
            (["root", "A", "b", "A"], [True, False, True, False]),
            (["root", "A", "b", "B"], [True, False, True, False]),
            (["root", "A", "b", "C"], [True, False, True, True]),
            (["root", "B"], [True, True]),
            (["root", "B", "a"], [True, True, False]),
            (["root", "B", "b"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "│  ", "├──"], ["root", "A", "a"]),
            (["", "│  ", "└──"], ["root", "A", "b"]),
            (["", "│  ", "   ", "├──"], ["root", "A", "b", "A"]),
            (["", "│  ", "   ", "├──"], ["root", "A", "b", "B"]),
            (["", "│  ", "   ", "└──"], ["root", "A", "b", "C"]),
            (["", "└──"], ["root", "B"]),
            (["", "   ", "├──"], ["root", "B", "a"]),
            (["", "   ", "└──"], ["root", "B", "b"]),
        ]

    def test_row_formatting_ex3(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "B"], [True, False]),
            (["root", "C"], [True, False]),
            (["root", "C", "a"], [True, False, False]),
            (["root", "C", "b"], [True, False, False]),
            (["root", "C", "c"], [True, False, False]),
            (["root", "C", "c", "A"], [True, False, False, False]),
            (["root", "C", "c", "B"], [True, False, False, False]),
            (["root", "C", "c", "C"], [True, False, False, False]),
            (["root", "C", "c", "D"], [True, False, False, False]),
            (["root", "C", "c", "D", "a"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "b"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "c"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "d"], [True, False, False, False, False]),
            (
                ["root", "C", "c", "D", "d", "A"],
                [True, False, False, False, False, False],
            ),
            (
                ["root", "C", "c", "D", "d", "B"],
                [True, False, False, False, False, False],
            ),
            (
                ["root", "C", "c", "D", "d", "C"],
                [True, False, False, False, False, True],
            ),
            (
                ["root", "C", "c", "D", "d", "C", "a"],
                [True, False, False, False, False, True, True],
            ),
            (["root", "C", "c", "D", "e"], [True, False, False, False, True]),
            (
                ["root", "C", "c", "D", "e", "A"],
                [True, False, False, False, True, True],
            ),
            (["root", "C", "c", "E"], [True, False, False, True]),
            (["root", "C", "c", "E", "a"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "b"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "c"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "d"], [True, False, False, True, True]),
            (["root", "C", "d"], [True, False, False]),
            (["root", "C", "e"], [True, False, True]),
            (["root", "D"], [True, True]),
            (["root", "D", "a"], [True, True, False]),
            (["root", "D", "b"], [True, True, False]),
            (["root", "D", "c"], [True, True, False]),
            (["root", "D", "d"], [True, True, False]),
            (["root", "D", "e"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "├──"], ["root", "B"]),
            (["", "├──"], ["root", "C"]),
            (["", "│  ", "├──"], ["root", "C", "a"]),
            (["", "│  ", "├──"], ["root", "C", "b"]),
            (["", "│  ", "├──"], ["root", "C", "c"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "A"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "B"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "C"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "D"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "a"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "b"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "c"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "d"]),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "├──"],
                ["root", "C", "c", "D", "d", "A"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "├──"],
                ["root", "C", "c", "D", "d", "B"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "└──"],
                ["root", "C", "c", "D", "d", "C"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "   ", "└──"],
                ["root", "C", "c", "D", "d", "C", "a"],
            ),
            (["", "│  ", "│  ", "│  ", "└──"], ["root", "C", "c", "D", "e"]),
            (
                ["", "│  ", "│  ", "│  ", "   ", "└──"],
                ["root", "C", "c", "D", "e", "A"],
            ),
            (["", "│  ", "│  ", "└──"], ["root", "C", "c", "E"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "a"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "b"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "c"]),
            (["", "│  ", "│  ", "   ", "└──"], ["root", "C", "c", "E", "d"]),
            (["", "│  ", "├──"], ["root", "C", "d"]),
            (["", "│  ", "└──"], ["root", "C", "e"]),
            (["", "└──"], ["root", "D"]),
            (["", "   ", "├──"], ["root", "D", "a"]),
            (["", "   ", "├──"], ["root", "D", "b"]),
            (["", "   ", "├──"], ["root", "D", "c"]),
            (["", "   ", "├──"], ["root", "D", "d"]),
            (["", "   ", "└──"], ["root", "D", "e"]),
        ]


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
                char
                for char in format_signature(myfunc1, verbosity=verbosity)
                if char != " "
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

        assert format_signature(myfunc2, verbosity=verbosity) == expected

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

        assert format_signature(Counter.most_common, verbosity=verbosity) == expected

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
                for char in format_signature(
                    myclass.method_bound_to_myclass, verbosity=verbosity
                )
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
                    myclass.static_method_bound_to_myclass, verbosity=verbosity
                )
                if char != " "
            )
            == expected
        )

    @staticmethod
    def test_width_restriction():
        """Test that the width is always respected."""

        func = treedoctestpackage.module.func_many_long_args

        generator = itertools.product(list(range(15, 100)), [0, 1, 2, 3, 4])
        for width, verbosity in generator:
            formatted_signature = format_signature(
                func, width=width, verbosity=verbosity
            )
            assert len(formatted_signature) <= width


if __name__ == "__main__":
    import pytest

    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
