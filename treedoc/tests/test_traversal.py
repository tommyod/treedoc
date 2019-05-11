#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:38:59 2019

@author: tommy
"""

import pytest
import itertools


from treedoc.traversal import ObjectTraverser

import treedoctestpackage as testpackage
import treedoctestpackage.subpackage as subtestpackage
from treedoctestpackage import module


def test_traversal():
    assert True


@pytest.mark.parametrize("modules", [True, False])
def test_recusion_subpackages(modules):
    """Regardless of what the `modules` flag says, the following should hold."""

    traverser = ObjectTraverser(subpackages=True, modules=modules)
    assert traverser.recurse_to_child_object(obj=testpackage, child_obj=subtestpackage)

    traverser = ObjectTraverser(subpackages=False, modules=modules)
    assert not traverser.recurse_to_child_object(
        obj=testpackage, child_obj=subtestpackage
    )


@pytest.mark.parametrize(
    "subpackages, modules", itertools.product([True, False], [True, False])
)
def test_recusion_subpackages_never_up(subpackages, modules):
    """As a fail-safe, we assure that recursion will never go up."""

    traverser = ObjectTraverser(subpackages=subpackages, modules=modules)
    # Notice that the arguments are switched and in the wrong order
    assert not traverser.recurse_to_child_object(
        obj=subtestpackage, child_obj=testpackage
    )


@pytest.mark.parametrize("subpackages", [True, False])
def test_recusion_modules(subpackages):
    """Regardless of what the `subpackages` flag says, the following should hold."""

    traverser = ObjectTraverser(subpackages=subpackages, modules=True)
    assert traverser.recurse_to_child_object(obj=testpackage, child_obj=module)

    traverser = ObjectTraverser(subpackages=subpackages, modules=False)
    assert not traverser.recurse_to_child_object(obj=testpackage, child_obj=module)


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
