#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:20:49 2019

@author: tommy
"""

import operator

import treedoctestpackage
from treedoc.utils import descend_from_package, ispackage, resolve_object, format_signature


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
    
    
def test_signature():
    ''' 
    Test that formatting signature works.
    '''
    
    def myfunc(a: float=4.2, b: int=42, *args, **kwargs):
        return None    
    
    assert format_signature(myfunc, verbosity=0) == ''
    assert format_signature(myfunc, verbosity=1) == '(...)'
    assert format_signature(myfunc, verbosity=2) == '(a, b, *args, **kwargs)'
    assert format_signature(myfunc, verbosity=3) == '(a=4.2, b=42, *args, **kwargs)'
    assert format_signature(myfunc, verbosity=4) == '(a: float=4.2, b: int=42, *args, **kwargs)'
    
    import collections import Counter
   
    assert format_signature(Counter.most_common, 0) == ""
    assert format_signature(Counter.most_common, 1) == "(...)"
    assert format_signature(Counter.most_common, 2) == "(self, n)"
    assert format_signature(Counter.most_common, 3) == "(self, n=None)"
    assert format_signature(Counter.most_common, 4) == "(self, n=None)"


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
